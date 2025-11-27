use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;
use std::error::Error;
use reqwest::header::{USER_AGENT, AUTHORIZATION};
use chrono::{DateTime, Utc};

#[derive(Debug, Deserialize, Serialize)]
struct BlogIndex {
    posts: Vec<BlogPost>,
}

#[derive(Debug, Deserialize, Serialize)]
struct BlogPost {
    slug: String,
    repo: String,
    date: String,
    path: String,
}

#[derive(Debug, Deserialize)]
struct GithubRelease {
    tag_name: String,
    published_at: Option<String>,
    body: Option<String>,
    html_url: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    env_logger::init();

    let index_path = "website/public/blog_index.json";
    if !Path::new(index_path).exists() {
        println!("Blog index not found at {}", index_path);
        return Ok(());
    }

    let content = fs::read_to_string(index_path)?;
    let index: BlogIndex = serde_json::from_str(&content)?;

    let client = reqwest::Client::new();
    let token = std::env::var("GITHUB_TOKEN").ok();

    for post in index.posts {
        if post.repo.is_empty() {
            continue;
        }

        println!("Checking updates for {}...", post.repo);

        let url = format!("https://api.github.com/repos/{}/releases/latest", post.repo);
        let mut request = client.get(&url)
            .header(USER_AGENT, "bestof-opensource-bot");

        if let Some(t) = &token {
            request = request.header(AUTHORIZATION, format!("Bearer {}", t));
        }

        let response = request.send().await;

        match response {
            Ok(resp) => {
                if resp.status().is_success() {
                    let release: GithubRelease = resp.json().await?;

                    if let Some(published_at) = release.published_at {
                        // Parse dates
                        let release_date = DateTime::parse_from_rfc3339(&published_at)?.with_timezone(&Utc);

                        // Simple check: is release newer than post date?
                        // Note: post.date is YYYY-MM-DD (NaiveDate), we need to be careful.
                        // For now, just printing.
                        println!("  Latest release: {} ({})", release.tag_name, release_date);

                        // TODO: Logic to check if this update is already in the MD file
                        // and append if not.
                    }
                } else {
                    println!("  Failed to fetch release: {}", resp.status());
                }
            }
            Err(e) => println!("  Error checking {}: {}", post.repo, e),
        }
    }

    Ok(())
}
