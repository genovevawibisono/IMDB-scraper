# IMDB Web Scraper

## Project Overview

This Python-based IMDB Web Scraper is a powerful tool designed to extract comprehensive information about actors and movies/TV shows directly from IMDB. The application provides an interactive command-line interface that allows users to retrieve detailed insights, making it valuable for entertainment research, media analysis, and professional content exploration.

## 🌟 Key Features

### Actor Information Retrieval
- Fetch detailed actor profiles
- Extract actor's biography
- List movies and shows an actor is known for
- Retrieve upcoming projects
- Access complete acting credits

### Movie/Show Information Extraction
- Obtain show/movie ratings
- Retrieve show descriptions
- List creators and cast members
- Support for both movies and TV shows

## 🛠 Technical Specifications

### Technologies Used
- Python 3.x
- BeautifulSoup4 for web scraping
- Requests library for HTTP interactions
- Regular expressions for data parsing

### Dependencies
- beautifulsoup4
- requests
- re (built-in)
- sys (built-in)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/genovevawibisono/imdb-scraper.git

# Navigate to the project directory
cd imdb-scraper

# Install required dependencies
pip install beautifulsoup4 requests
```

## 💡 Usage Examples

### Scraping Actor Information
```
Enter choice: 1
Enter a name: Tom Hanks

# The script will retrieve:
# - Actor ID
# - About information
# - Known for titles
# - Upcoming projects
# - Previous credits
```

### Scraping Show/Movie Information
```
Enter choice: 2
Enter a title: Breaking Bad

# The script will retrieve:
# - Show/Movie ID
# - Rating
# - Description
# - Creators
# - Cast members
```

## 🔍 Research and Professional Applications

### For Researchers
- Media Studies
- Entertainment Industry Analysis
- Content Trend Tracking
- Academic Research on Film and Television

### For Professionals
- Talent Scouting
- Production Planning
- Content Recommendation Systems
- Market Research in Entertainment

## 🛡️ Ethical Considerations
- Respects IMDB's robots.txt
- Uses appropriate user-agent headers
- Implements responsible web scraping practices

## 🔧 Potential Improvements
- Add rate limiting
- Implement more robust error handling
- Create configuration for custom scraping
- Develop API or export functionality

## 📄 License
MIT License

## 👥 Contributing
Contributions, issues, and feature requests are welcome. Feel free to check reach out via github.
