from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Clear old users if needed (optional)
    db.drop_all()
    db.create_all()

    users = [
        User(
            email="jane@example.com",
            first_name="Jane",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-123-4567",
            city="San Francisco",
            state="CA",
            tags="python,flask,design",
            interests="reading,hiking,chess",
            seo="SEO Scholars"),

        User(
            email="bob@example.com",
            first_name="Bob",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-234-5678",
            city="New York",
            state="NY",
            tags="javascript,node,express",
            interests="reading,traveling,hiking",
            seo="SEO Career"),

        User(
            email="alice@example.com",
            first_name="Alice",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-345-6789",
            city="Austin",
            state="TX",
            tags="react,frontend,css",
            interests="cooking,photography,movies",
            seo="SEO Tech Developer"),

        User(
            email="mike@example.com",
            first_name="Mike",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-456-7890",
            city="Chicago",
            state="IL",
            tags="java,spring,backend",
            interests="music,art,drawing", 
            seo="SEO Alternative Investments"),

        User(
            email="sara@example.com",
            first_name="Sara",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-567-8901",
            city="Seattle",
            state="WA",
            tags="python,data,ml",
            interests="gaming,streaming,anime",
            seo="SEO Law"),

        User(
            email="david@example.com",
            first_name="David",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-678-9012",
            city="Boston",
            state="MA",
            tags="go,cloud,devops",
            interests="sports,running,fitness",
            seo="SEO Scholars, SEO Career"),
            

        User(
            email="lisa@example.com",
            first_name="Lisa",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-789-0123",
            city="Denver",
            state="CO",
            tags="design,ux,figma",
            interests="gardening,diy,crafts",
            seo="SEO Tech Developer, SEO Career"),

        User(
            email="tom@example.com",
            first_name="Tom",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-890-1234",
            city="Portland",
            state="OR",
            tags="vue,frontend,javascript",
            interests="dancing,singing,acting", 
            seo="SEO Alternative Investments"),

        User(
            email="rachel@example.com",
            first_name="Rachel",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-901-2345",
            city="Atlanta",
            state="GA",
            tags="ai,nlp,python",
            interests="tech,gadgets,blogging",
            seo="SEO Scholars"),

        User(
            email="kevin@example.com",
            first_name="Kevin",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-012-3456",
            city="Miami",
            state="FL",
            tags="nodejs,backend,graphql",
            interests="volunteering,mentoring,public speaking", 
            seo="SEO Career"),

        User(
            email="nina@example.com",
            first_name="Nina",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-111-2222",
            city="Dallas",
            state="TX",
            tags="cybersecurity,linux,networking",
            interests="fashion,shopping,makeup", 
            seo="SEO Tech Developer"),

        User(
            email="sam@example.com",
            first_name="Sam",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-222-3333",
            city="Los Angeles",
            state="CA",
            tags="flutter,dart,mobile",
            interests="reading,traveling,hiking", 
            seo="SEO Alternative Investments"),

        User(
            email="olivia@example.com",
            first_name="Olivia",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-333-4444",
            city="Philadelphia",
            state="PA",
            tags="data,sql,tableau",
            interests="cooking,photography,movies", 
            seo="SEO Law"),

        User(
            email="tony@example.com",
            first_name="Tony",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-444-5555",
            city="Phoenix",
            state="AZ",
            tags="devops,docker,aws",
            interests="music,art,drawing", 
            seo="SEO Scholars, SEO Career"),

        User(
            email="emily@example.com",
            first_name="Emily",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-555-6666",
            city="Detroit",
            state="MI",
            tags="marketing,seo,analytics",
            interests="gaming,streaming,anime", 
            seo="SEO Tech Developer, SEO Career"),

        User(
            email="chris@example.com",
            first_name="Chris",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-666-7777",
            city="Columbus",
            state="OH",
            tags="java,kotlin,android",
            interests="sports,running,fitness",
            seo="SEO Alternative Investments"),

        User(
            email="emma@example.com",
            first_name="Emma",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-777-8888",
            city="Minneapolis",
            state="MN",
            tags="python,web,scraping",
            interests="gardening,diy,crafts", 
            seo="SEO Scholars"),

        User(
            email="dan@example.com",
            first_name="Dan",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-888-9999",
            city="Salt Lake City",
            state="UT",
            tags="react,typescript,redux",
            interests="dancing,singing,acting", 
            seo="SEO Career"),

        User(
            email="julia@example.com",
            first_name="Julia",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-999-0000",
            city="Baltimore",
            state="MD",
            tags="project,agile,management",
            interests="tech,gadgets,blogging", 
            seo="SEO Tech Developer"),

        User(
            email="ryan@example.com",
            first_name="Ryan",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-000-1111",
            city="Las Vegas",
            state="NV",
            tags="firebase,mobile,js",
            interests="volunteering,mentoring,public speaking", 
            seo="SEO Alternative Investments"),

        User(
            email="megan@example.com",
            first_name="Megan",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-123-6789",
            city="Tampa",
            state="FL",
            tags="design,ux,ui",
            interests="fashion,shopping,makeup", 
            seo="SEO Law"),

        User(
            email="henry@example.com",
            first_name="Henry",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-234-7890",
            city="San Diego",
            state="CA",
            tags="python,api,rest",
            interests="reading,traveling,hiking", 
            seo="SEO Scholars, SEO Career"),

        User(
            email="mia@example.com",
            first_name="Mia",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-345-8901",
            city="Cleveland",
            state="OH",
            tags="sql,databases,data",
            interests="cooking,photography,movies", 
            seo="SEO Tech Developer, SEO Career"),

        User(
            email="leo@example.com",
            first_name="Leo",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-456-9012",
            city="Indianapolis",
            state="IN",
            tags="html,css,js",
            interests="music,art,drawing", 
            seo="SEO Alternative Investments"),

        User(
            email="grace@example.com",
            first_name="Grace",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-567-0123",
            city="Charlotte",
            state="NC",
            tags="php,laravel,mysql",
            interests="gaming,streaming,anime", 
            seo="SEO Scholars"),

        User(
            email="zach@example.com",
            first_name="Zach",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-678-1234",
            city="Kansas City",
            state="MO",
            tags="c#,dotnet,api",
            interests="sports,running,fitness", 
            seo="SEO Career"),
        
        User(
            email="hannah@example.com",
            first_name="Hannah",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-789-2345",
            city="Raleigh",
            state="NC",
            tags="data,excel,statistics",
            interests="gardening,diy,crafts", 
            seo="SEO Tech Developer"),

        User(
            email="jack@example.com",
            first_name="Jack",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-890-3456",
            city="Orlando",
            state="FL",
            tags="security,python,networking",
            interests="dancing,singing,acting", 
            seo="SEO Alternative Investments"),

        User(
            email="tina@example.com",
            first_name="Tina",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-901-4567",
            city="Nashville",
            state="TN",
            tags="python,jupyter,ai",
            interests="tech,gadgets,blogging", 
            seo="SEO Law"),

        User(
            email="mark@example.com",
            first_name="Mark",
            password=generate_password_hash(
                "password123", method='pbkdf2:sha256'),
            phone_number="555-012-5678",
            city="Pittsburgh",
            state="PA",
            tags="flask,sqlalchemy,web",
            interests="volunteering,mentoring,public speaking", 
            seo="SEO Tech Developer, SEO Career")
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()

    print("Dummy users added to the database!")
