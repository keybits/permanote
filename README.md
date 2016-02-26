
# Permanote

<img title="Permanote dolphin logo" alt="Permanote dolphin logo" align="right" src=".sandstorm/app-graphics/permanote-dolphin150.png">

A personal note-taking application designed for Sandstorm.

It has the features I want. I use it for keeping a journal and recording technical tips and documentation when I need longer form notes. For me it has replaced Evernote and Google Keep - although it clearly doesn't have many of Evernote's features. I still use Google Keep for small quick notes that I need to be synced with mobile devices.

## Warning and help appreciated

This was hacked together over a weekend - please consider it Beta software and don't trust important data just yet. The code is horrible in many places! Pull requests gratefully received if you'd like to clean anything up before I get there.

## Features

- Markdown editing for notes
- Copy and paste or drag and drop image uploading
- Full text search
- Tags
- Syntax highlighting
- ~~Rich media embeds (e.g. YouTube videos)~~ removed for now
- Archive old notes
- Keyboard shortcuts to create new note and submit note when done editing

## Non-features

- No notebooks - create a new Sandstorm grain
- No user accounts or access control ([because it's a Sandstorm app](https://docs.sandstorm.io/en/latest/developing/handbook/#does-not-implement-user-accounts-or-access-control))
- No WYSIWIG editing - you need to write your own Markdown
- No syncing or offline capability

## Technology

- Flask
- Peewee
- SQLite
- jquery inline-attachment

## Credits

### Charles Leifer

A lot of the code for this application was lifted directly from this blog post by Charles Leifer: <http://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/>

Many thanks to Charles for his helpful blog posts and for creating excellent support for SQLite with his Peewee ORM. This makes an excellent choice for developing Sandstorm apps.

### Logo

The dolphin logo is from the Twitter twemoji collection: https://github.com/twitter/twemoji

**Why a dolphin for the logo?** Evernote use an elephant for their logo because elephants are known to have good memories.

Apparently [dolphins have even better memories](http://news.nationalgeographic.com/news/2013/08/130806-dolphins-memories-animals-science-longest/)
