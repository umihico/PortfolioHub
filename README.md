# thumbnailed-portfolio-websites
GIF Screenshots of everybody's [#portfolio-websites](https://github.com/topics/portfolio-website) on github  
**[http://umihi.co/thumbnailed-portfolio-websites/](http://umihi.co/thumbnailed-portfolio-websites/)**  

### sister website:
**[http://umihi.co/thumbnailed-personal-websites/](http://umihi.co/thumbnailed-personal-websites/)**  
([#personal-websites](https://github.com/topics/personal-website) version)  

### How to add my portfolio?
+ Add topic #portfolio-websites or #personal-website in your repository.
+ Add portfolio url in your repository, or your repository name is YOURNAME.github.io
+ Please wait till next crawling.

![readme_img](/readme_img.jpg)

### Skillset calculation formula
1. exacts 'language' and 'size' from https://api.github.com/users/USERNAME/repos?per_page=100&page=1&sort=pushed  (this means one repository can have only one language)
2. weighting size by last-pushed day sort index(1-100), so `size=1+(1/index)*size`.
3. distribute 100 points according to size.


### Where is my gif?
+ Please check [all information here](https://umihico.github.io/thumbnailed-portfolio-websites/database.html) and search your name. Feel free to create issue if you don't find.
