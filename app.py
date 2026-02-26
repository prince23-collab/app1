from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import NotFound
from jinja2 import Environment, FileSystemLoader

# ------------------------
# Basic setup
# ------------------------
BASE_URL = "/it22_escrupolo/webapps/app4"

env = Environment(loader=FileSystemLoader("templates"))

def render(template, **context):
    context.update({
        "base_url": BASE_URL,        
    })
    return Response(
        env.get_template(template).render(**context),
        content_type="text/html"
    )

# ------------------------
# Routes
# ------------------------
url_map = Map([
    Rule("/", endpoint="home"),
    Rule("/products", endpoint="products"),
    Rule("/services", endpoint="services"),
    Rule("/company", endpoint="company"),
    Rule("/history", endpoint="history"),
    Rule("/contactus", endpoint="contactus"),
    Rule("/register", endpoint="register"),
])

# ------------------------
# View functions
# ------------------------
def home(request):

    return render("home.html")

# ------------------------
def products(request):

    product_items = [
    {
        "id": 1,
        "name": "Gaming Laptop",
        "brand": "Dell",
        "price": 1500,
        "stock": 10
    },
    {
        "id": 2,
        "name": "Mechanical Keyboard",
        "brand": "Logitech",
        "price": 120,
        "stock": 25
    },
    {
        "id": 3,
        "name": "Wireless Mouse",
        "brand": "Razer",
        "price": 80,
        "stock": 30
    },
    {
        "id": 4,
        "name": "27-inch Monitor",
        "brand": "ASUS",
        "price": 300,
        "stock": 15
    },
    {
        "id": 5,
        "name": "External Hard Drive 2TB",
        "brand": "Seagate",
        "price": 90,
        "stock": 20
    },
    {
        "id": 6,
        "name": "Gaming Headset",
        "brand": "HyperX",
        "price": 100,
        "stock": 18
    },
    {
        "id": 7,
        "name": "Graphics Card RTX 4070",
        "brand": "NVIDIA",
        "price": 600,
        "stock": 5
    },
    {
        "id": 8,
        "name": "SSD 1TB NVMe",
        "brand": "Samsung",
        "price": 120,
        "stock": 22
    },
    {
        "id": 9,
        "name": "Laptop Cooling Pad",
        "brand": "Cooler Master",
        "price": 40,
        "stock": 12
    },
    {
        "id": 10,
        "name": "USB-C Hub",
        "brand": "Anker",
        "price": 35,
        "stock": 28
    }]
    return render("products.html",product_items = product_items)


def services(request):
    return render("services.html")

def company(request):
    company_info = [
    {
        "name": "Tech Solutions Inc.",
        "address": "1234 Tech Street, Silicon Valley, CA 94043",
        "phone": "+1 (555) 123-4567",
        "email": "contact@techsolutions.com"
    }]
    return render("company.html", company_info = company_info)

def history(request):
    History = [
    {
        "year": 2010,
        "event": "Company founded by a group of tech enthusiasts."
    },
    {
        "year": 2012,
        "event": "Launched our first product, a cloud-based project management tool."
    },
    {
        "year": 2015,
        "event": "Expanded our services to include IT consulting and support."
    },
    {
        "year": 2018,
        "event": "Opened a new office in New York City to better serve our East Coast clients."
    },
    {
        "year": 2020,
        "event": "Adapted to remote work and continued providing excellent service during the pandemic."
    }
    ]
    return render("history.html", History = History)

def contactus(request):
     
    Contact_info = [
    {
        "dept": "Customer Support", 
        "phone": "+1 (555) 987-6543",
        "email": "support@techsolutions.com"
    },
    {   "dept": "Sales Inquiries",
        "phone": "+1 (555) 555-1234",
        "email": "sales@techsolutions.com"
    },
    ]
    return render("contactus.html", Contact_info=Contact_info)

def register(request):
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(email, password)

        return render("register.html", message=f"Registration is submitted! Welcome, {email}")

    return render("register.html")

    return render(request, "register.html")
# ------------------------
# WSGI app
# ------------------------
@Request.application
def app(request):
    adapter = url_map.bind_to_environ(request.environ)

    try:
        endpoint, values = adapter.match()
        return globals()[endpoint](request, **values)
    except NotFound:
        return Response("404 Not Found", status=404)
