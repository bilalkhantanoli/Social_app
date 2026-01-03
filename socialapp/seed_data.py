import os
import django
import random
from django.core.files import File
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialapp.settings')
django.setup()

from django.contrib.auth.models import User
from feed.models import Post, Profile, Comment, Like

def create_users():
    users = []
    names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan']
    for name in names:
        username = name.lower()
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=f'{username}@example.com', password='password123')
            # Profile created by signal, just update bio
            user.profile.bio = f"Hello, I'm {name}! I love photography and travel."
            user.profile.save()
            print(f"Created user: {username}")
            users.append(user)
        else:
            print(f"User {username} already exists")
            users.append(User.objects.get(username=username))
    return users

def create_posts(users):
    titles = [
        "Amazing Sunset", "Mountain Adventure", "City Lights", "Morning Coffee", 
        "Code Life", "Weekend Vibes", "Nature Walk", "Throwback", "New Project", "Relaxation"
    ]
    
    # Path to a dummy image (we will ensure this exists before running)
    image_path = os.path.join(settings.BASE_DIR, 'media', 'post_images', 'nature_post_image.png')

    
    for i in range(15):
        user = random.choice(users)
        title = random.choice(titles)
        content = f"This is a sample post about {title}. Hope you like it! #{title.replace(' ', '')}"
        
        post = Post.objects.create(user=user, title=title, content=content)
        
        # Attach image if exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                post.image.save(f'post_{i}.png', File(f), save=True)

        
        print(f"Created post: {title} by {user.username}")

        # Add interactions
        # Likes
        for u in users:
            if random.choice([True, False]):
                Like.objects.create(user=u, post=post)
        
        # Comments
        for _ in range(random.randint(0, 3)):
            c_user = random.choice(users)
            Comment.objects.create(post=post, user=c_user, content="Great shot! 🔥")

if __name__ == "__main__":
    print("Seeding data...")
    users = create_users()
    create_posts(users)
    print("Done!")
