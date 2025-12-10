# Linkblog

This project is a Jekyll-based blog that automatically generates daily posts containing a curated list of Twitter links.

## How It Works

The blog is updated by a set of scripts that fetch links and create new posts.

*   **`scripts/list_twitter_links_by_date.py`**: This Python script is the core of the post generation. It fetches links for a given date and formats them into a Markdown file, creating a new post in the `_posts` directory.
*   **`scripts/daily_post.sh`**: This shell script automates the process by calling the Python script for the previous day, and then committing and pushing the new post to the GitHub repository.

The script `list_twitter_links_by_date.py` depends on a custom Python module `socialModules.modulePublicationCache` which is not included in this repository. This module is responsible for fetching the actual link data.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd linkblog
    ```

2.  **Install Ruby and Bundler:**
    Make sure you have Ruby (version 3.1 or as specified in `.github/workflows/jekyll.yml`) and Bundler installed.
    ```bash
    gem install bundler
    ```

3.  **Install Jekyll and other gems:**
    ```bash
    bundle install
    ```

4.  **Install Python:**
    Ensure you have Python 3 installed.

5.  **Set up the custom Python module:**
    You will need to provide the `socialModules` Python module, as it is not included in this repository. This module should be placed where it can be imported by the `list_twitter_links_by_date.py` script.

## Usage

### Local Development

To serve the site locally for testing or previewing changes:

```bash
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000`.

### Creating a New Post

To manually generate a new post for a specific date:

```bash
python3 scripts/list_twitter_links_by_date.py YYYY-MM-DD
```

To run the automated daily process:

```bash
bash scripts/daily_post.sh
```
This will create a post for yesterday, add it to git, commit it, and push it to the remote repository.

## Deployment

Deployment is handled automatically by a GitHub Actions workflow defined in `.github/workflows/jekyll.yml`.

Every push to the `main` branch triggers the workflow, which builds the Jekyll site and deploys it to GitHub Pages.
