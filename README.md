# Joseph Lemaitre — personal website

A static Jekyll website migrated from the WordPress export dated September 12, 2026. It uses a small custom academic layout inspired by the reference websites, without a third-party theme.

## Preview and build

Jekyll requires a recent Ruby and Bundler. On this Mac, Homebrew Ruby has been installed and is selected automatically by `scripts/jekyll.sh`. Your system Ruby and shell configuration were not changed.

Install dependencies (already done on this Mac):

```sh
export PATH="/opt/homebrew/opt/ruby/bin:$PATH" # Homebrew Apple Silicon Macs only
BUNDLE_PATH=vendor/bundle bundle install
```

Start a preview:

```sh
bash scripts/jekyll.sh serve --port 1313
```

Open http://localhost:1313. Stop the server with Ctrl+C. Build and check:

```sh
JEKYLL_ENV=production bash scripts/jekyll.sh build
python3 scripts/check_site.py
```

Only deploy `dist/`. The domain in `_config.yml` is the original `https://josephlemaitre.com`; change `url` when using another production domain. This migration does not change WordPress or DNS. Keep `baseurl` empty for root-domain hosting. Imported image and page links currently assume root-domain hosting.

## Editing

- `site/index.md`: biography / homepage.
- `site/_posts/`: seven published posts, named `YYYY-MM-DD-slug.md`.
- `site/pages/`: three other published pages, including the posts index.
- `draft/`: five unpublished drafts (two posts and three pages).
- `private/`: one private post, retained separately.
- `site/wp-content/uploads/`: recovered public images at their original URL paths.
- `site/assets/css/site.css`: visual styling.
- `site/_layouts/` and `site/_includes/`: HTML templates.
- `_config.yml`: site configuration, navigation and build settings.

Jekyll reads only `site/`. The `draft/` and `private/` folders and the XML archive are outside that source directory, excluded from Git, and never copied to the build, even when draft rendering is enabled. The Markdown also has `published: false`. To publish a draft deliberately, copy it into `site/_posts/` with a `YYYY-MM-DD-slug.md` filename, set `layout: post`, `published: true`, and `draft: false`, and review its date and URL. Use `site/pages/` and `layout: page` for a page draft.

## Migration

All 17 posts/pages have been converted to Markdown. Dates, slugs, categories, tags, original titles, statuses, URLs and WordPress IDs are retained in front matter. Explicit permalinks preserve the original published URLs. Original wording, including unfinished sentences in content marked published by WordPress, is preserved.

The original XML remains untouched in `wordpress archive/`. It retains comments, attachments, blocks and templates that are not part of the static site. WordPress layout wrappers are removed from Markdown; social-link blocks are converted to links. The Atomic posts page uses the `atomic` category to replace WordPress's dynamic query. Comments, forms, the admin area and plugins are not part of the static site.

`migration-manifest.json` maps each entry to its Markdown file. `media-manifest.json` records all five recovered public images. Unpublished drafts still reference remote images, including WordPress theme demonstration art; their original markup remains in the XML.

`scripts/import_wordpress.py` uses Python 3 and Pandoc to repeat extraction without overwriting existing Markdown. `scripts/recover_media.py` fetches public images and rewrites their URLs locally. Neither tool is required for normal builds. Liquid processing is disabled for imported writing so code examples remain literal.

Framework references:
- Daniel McDonald uses Quarto: https://github.com/dajmcdon/dajmcdon.github.io/blob/main/_quarto.yml
- Rob Williams's guide uses Jekyll / Academic Pages: https://jayrobwilliams.com/posts/2020/06/academic-website/
- This website uses Jekyll: https://jekyllrb.com/
