# Menu

- <a href="/README.md">Project Breifing</a>
- Application Testing - <b>You are here</b>
---

# ReviewScraper - Testing

### Buy Why?

I'm trying to build a GitHub profile that demonstrates my experience that I've been developing since 2009, to demonstrate my clean and detailed code. I'm told that developing by testing is an important skill.

---

### Testing


| Test Case                                   | Expected Result                                                                  | Actual Result                            | Pass/Fail |
|:--------------------------------------------|:---------------------------------------------------------------------------------|:-----------------------------------------|:---------:|
| Requirements fit the project                | Python command can run reviewscrape.py without complaint of missing modules      | Python program ran just fine             | ✅        |
| Launch params vs. prompt input              | Should respond to -url param, or if ommited, prompt user for the URL at runtime  | Both scenarios work                      | ✅        |
| Different behaviour depending on URL domain | Console should print out the detected domain to demonstrate sucsess              | I can see Techradar in the console       | ✅        |
| Able to scrape the websites desired content | Console should output the parts we've defined in code, and ignore the rest.      | Console outputs the good stuff.          | ✅        |
