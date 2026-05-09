(function () {
    var storageKey = 'cybercore_course_progress';
    var course = document.querySelector('[data-progress-course]');
    var courseCards = Array.prototype.slice.call(document.querySelectorAll('[data-course-card]'));

    function loadProgress() {
        try {
            return JSON.parse(localStorage.getItem(storageKey)) || {};
        } catch (error) {
            return {};
        }
    }

    function saveProgress(progress) {
        localStorage.setItem(storageKey, JSON.stringify(progress));
    }

    function countCompleted(courseProgress) {
        return Object.keys(courseProgress).filter(function (itemId) {
            return courseProgress[itemId] === 'complete';
        }).length;
    }

    function getCourseProgress(progress, courseId) {
        if (!progress[courseId]) {
            progress[courseId] = {};
        }

        return progress[courseId];
    }

    function updateCourseCards(progress) {
        courseCards.forEach(function (card) {
            var courseId = card.dataset.courseCard;
            var courseProgress = progress[courseId] || {};
            var completed = countCompleted(courseProgress);
            var total = Number(card.dataset.courseTotal) || 0;
            var percent = total ? Math.round((completed / total) * 100) : 0;
            var percentElement = card.querySelector('[data-course-percent]');
            var countElement = card.querySelector('[data-course-count]');
            var fillElement = card.querySelector('[data-course-fill]');

            if (percentElement) {
                percentElement.textContent = percent + '%';
            }

            if (countElement) {
                countElement.textContent = completed + '/' + total + ' Lekcji';
            }

            if (fillElement) {
                fillElement.style.width = percent + '%';
            }
        });
    }

    var progress = loadProgress();

    if (courseCards.length) {
        updateCourseCards(progress);
    }

    if (!course) {
        return;
    }

    function setItemStatus(item, status) {
        var button = item.querySelector('[data-status-toggle]');
        var isComplete = status === 'complete';

        item.dataset.status = status;
        item.classList.toggle('is-complete', isComplete);

        if (button) {
            button.textContent = isComplete ? 'Complete' : 'Do zrobienia';
            button.setAttribute('aria-pressed', String(isComplete));
        }
    }

    function updateSummary(items) {
        var completed = items.filter(function (item) {
            return item.dataset.status === 'complete';
        }).length;
        var total = items.length;
        var percent = total ? Math.round((completed / total) * 100) : 0;
        var summary = course.querySelector('[data-progress-summary]');
        var fill = course.querySelector('[data-progress-fill]');

        if (summary) {
            summary.textContent = completed + '/' + total + ' ukończone';
        }

        if (fill) {
            fill.style.width = percent + '%';
        }
    }

    var courseId = course.dataset.progressCourse;
    var items = Array.prototype.slice.call(course.querySelectorAll('[data-progress-item]'));
    var courseProgress = getCourseProgress(progress, courseId);

    items.forEach(function (item) {
        var itemId = item.dataset.progressItem;
        var status = courseProgress[itemId] || 'todo';
        var button = item.querySelector('[data-status-toggle]');

        setItemStatus(item, status);

        if (button) {
            button.addEventListener('click', function () {
                var nextStatus = item.dataset.status === 'complete' ? 'todo' : 'complete';

                courseProgress[itemId] = nextStatus;
                progress[courseId] = courseProgress;
                saveProgress(progress);
                setItemStatus(item, nextStatus);
                updateSummary(items);
                updateCourseCards(progress);
            });
        }
    });

    updateSummary(items);
}());
