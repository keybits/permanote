import os
import datetime
import urllib

from flask import (flash, redirect, render_template, request,
                   Response, url_for, jsonify, send_from_directory)
from flask import url_for as flask_url_for
from werkzeug.utils import secure_filename
from playhouse.flask_utils import get_object_or_404, object_list
from playhouse.sqlite_ext import *

from app import application
from models import Entry, Tag, EntryTags

# Make url_for use https for redirects on Sandstorm
def url_for(endpoint, **kwargs):
    if os.getenv('SANDSTORM'):
        kwargs.setdefault('_external', True)
        kwargs.setdefault('_scheme', 'https')
    return flask_url_for(endpoint, **kwargs)

@application.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())

    # The `object_list` helper will take a base query and then handle
    # paginating the results if there are more than 20. For more info see
    # the docs:
    # http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#object_list
    return object_list(
        'index.html',
        query,
        search=search_query,
        check_bounds=False)

@application.route('/archive/')
def archive():
    query = Entry.archive().order_by(Entry.timestamp.desc())
    return object_list('index.html', query, archive=archive)

@application.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry = Entry.create(
                title=request.form['title'],
                content=request.form['content'],
                archived=request.form.get('archived') or False)
            tags = request.form['tags'].split()
            # present is a check to see if the tag exists
            present = 0
            # add or create tags
            for tag in tags:
                for entrytag in entry.tags:
                    if tag == entrytag.tag:
                        present = 1
                if present == 0:
                    try:
                        thistag = Tag.get(Tag.tag == tag)
                        entry.tags.add(thistag)
                    except:
                        tag_obj, was_created = Tag.create_or_get(tag=tag)
                        EntryTags.create(tag=tag_obj, entry=entry)
                present = 0
            flash('Entry created successfully.', 'success')
            return redirect(url_for('detail', slug=entry.slug))
        # TODO Refactor the below and above to make it more DRY or not
        # to need to display seconds (e.g. add some kind of suffix if entry
        # already exists)
        elif request.form.get('content'):
            entry = Entry.create(
                title="{:%a %d %b %Y at %H:%M:%S}".format(datetime.datetime.now()),
                content=request.form['content'])
            flash('Note created successfully.', 'success')
            return redirect(url_for('detail', slug=entry.slug))
        else:
            flash('Content is required.', 'danger')
    return render_template('create.html')


@application.route('/<slug>/')
def detail(slug):
    query = Entry.all()
    entry = get_object_or_404(query, Entry.slug == slug)
    tags = ""
    for tag in entry.tags:
        tags = tags + " " + tag.tag
    return render_template('detail.html', entry=entry, tags=tags)


@application.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    tags = ""
    for tag in entry.tags:
        tags = tags + " " + tag.tag
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry.title = request.form['title']
            entry.content = request.form['content']
            entry.archived = request.form.get('archived') or False
            # convert the string of tags to a list
            tags = request.form['tags'].split()
            # present is a check to see if the tag exists
            present = 0
            # add or create tags
            for tag in tags:
                for entrytag in entry.tags:
                    if tag == entrytag.tag:
                        present = 1
                if present == 0:
                    try:
                        thistag = Tag.get(Tag.tag == tag)
                        entry.tags.add(thistag)
                    except:
                        tag_obj, was_created = Tag.create_or_get(tag=tag)
                        EntryTags.create(tag=tag_obj, entry=entry)
                present = 0
            # remove tags
            for entrytag in entry.tags:
                for tag in tags:
                    if entrytag.tag == tag:
                        present = 1
                if present == 0:
                    thistag = Tag.get(Tag.tag == entrytag.tag)
                    entry.tags.remove(thistag)
                present = 0
            entry.save()

            flash('Note updated successfully.', 'success')
            return redirect(url_for('detail', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')

    return render_template('edit.html', entry=entry, tags=tags)


@application.route('/tags/')
def taglist():
    count = fn.COUNT(EntryTags.id)
    tags_with_counts = (Tag
                        .select(Tag, count.alias('entry_count'))
                        .join(EntryTags)
                        .join(Entry)
                        .where(Entry.archived==False)
                        .group_by(Tag)
                        .order_by(count.desc(), Tag.tag))
    return object_list('taglist.html', tags_with_counts, check_bounds=False)


@application.route('/tag/<tag>/')
def thistag(tag):
    search_query = request.args.get('q')
    query = (Entry.public()
             .select()
             .join(EntryTags)
             .join(Tag)
             .where(
        (Tag.tag == tag))
             .order_by(Entry.timestamp.desc()))
    return object_list(
        'index.html',
        query,
        tag=tag,
        search=search_query,
        check_bounds=False)


@application.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            filenamedict = dict([("filename", os.path.join('/uploads/', filename))])
        else:
            filenamedict = dict([("error", "Error while uploading file")])
    # see http://stackoverflow.com/a/13089975/94908 for explanation of the below
    return jsonify(**filenamedict)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in application.config['ALLOWED_EXTENSIONS']


@application.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'],
                               filename)


@application.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    # We'll use this template filter in the pagination include. This filter
    # will take the current URL and allow us to preserve the arguments in the
    # querystring while replacing any that we need to overwrite. For instance
    # if your URL is /?q=search+query&page=2 and we want to preserve the search
    # term but make a link to page 3, this filter will allow us to do that.
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urllib.urlencode(querystring)


@application.errorhandler(404)
def not_found(exc):
    return Response('<h3>Not found</h3>'), 404
