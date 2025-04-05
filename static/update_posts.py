from os import listdir
from re import sub

# Define the locations for the posts folder and index markdown.
addrPostsShort = './posts'
addrPosts = './content/posts'
addrIndex = './content/_index.md'

# Create content for index.md based on posts folder.

def createRecentPosts(addrPosts, content = '') -> str:
    posts = [file for file in listdir(addrPosts) if file.endswith('.md') and not file.startswith('_')] # '_' Prevents _index.md from bein read as a post

    # Sort date order to allow for most recent posts
    posts.sort(reverse=True)

    for post in posts[:5]: # limited to 5 most recent posts
        title = post.replace('.md', '').replace('-', ' ').title()
        link = f'{addrPostsShort}/{post}'
        content += f'- [{title}]({link})\n'
    
    return content


# Reads _index.md
try:
    with open(addrIndex, 'r') as file:
        indexContent = file.read()
except FileNotFoundError:
    indexContent = ''

# Regex pattern for posts
postsPattern = r'## Recent posts\n\n(?:- \[.*?\]\(.*?\)\n)*'

# Remove existing posts to prevent duplicates. Uses regex to identify posts.
indexContent = sub(postsPattern, '', indexContent)

# For some reason removing the previous posts writes blank lines the the file, fix:
indexContent = sub(r'\n{3,}', '\n\n', indexContent)

recentPosts = createRecentPosts(addrPosts)

mergedContent = f"{indexContent}\n\n## Recent posts\n\n{recentPosts}"

try:
    with open(addrIndex, 'w') as file:
        file.write(mergedContent)
except FileNotFoundError:
    pass