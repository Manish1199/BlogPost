// static/main.js
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        const title = document.getElementById('title').value.trim();
        const content = document.getElementById('content').value.trim();
        const pubDate = document.getElementById('pub_date').value.trim();

        if (!title || !content || !pubDate) {
            alert('All fields must be filled out');
            event.preventDefault();
        }
    });
});
