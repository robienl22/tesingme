import website_checker

# Read the website.txt file and get a list of websites to check for proxies
with open("website.txt", "r") as f:
    websites = f.readlines()

website_checker.check_websites(websites)
