# Joseph Lemaitre — personal website

Converted from WordPress to Jekyll on September 12, 2026.

## Run locally

Install Ruby and Bundler, then install the dependencies:

```sh
# On Apple Silicon Macs with Homebrew Ruby:
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
BUNDLE_PATH=vendor/bundle bundle install
```

Start the website:

```sh
bash scripts/jekyll.sh serve --port 1313
```

Open http://localhost:1313. Stop the server with Ctrl+C.

Build the static website into `dist/`:

```sh
JEKYLL_ENV=production bash scripts/jekyll.sh build
```
