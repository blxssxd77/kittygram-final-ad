document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.share-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var url = btn.dataset.url;
            if (navigator.share) {
                navigator.share({ url: url });
            } else if (navigator.clipboard) {
                navigator.clipboard.writeText(url).then(function () {
                    alert('Ссылка скопирована');
                });
            } else {
                prompt('Скопируйте ссылку:', url);
            }
        });
    });

    var modal = document.getElementById('contacts-modal');
    if (modal) {
        var closeBtn = document.getElementById('modal-close');
        document.querySelectorAll('.contacts-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                document.getElementById('modal-email').textContent =
                    'Email: ' + (btn.dataset.email || '—');
                document.getElementById('modal-phone').textContent =
                    'Телефон: ' + (btn.dataset.phone || '—');
                var github = btn.dataset.github;
                document.getElementById('modal-github').innerHTML =
                    github ? 'GitHub: <a href="' + github + '" target="_blank">' + github + '</a>' : 'GitHub: —';
                modal.classList.remove('hidden');
            });
        });
        closeBtn.addEventListener('click', function () {
            modal.classList.add('hidden');
        });
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }
});
