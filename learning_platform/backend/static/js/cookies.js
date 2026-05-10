(function () {
    var storageKey = 'cybercore_course_progress';
    var course = document.querySelector('[data-progress-course]');
    var courseCards = Array.prototype.slice.call(document.querySelectorAll('[data-course-card]'));
    var filterContainer = document.querySelector('[data-course-filters]');
    var filterButtons = Array.prototype.slice.call(document.querySelectorAll('[data-course-filter]'));
    var emptyState = document.querySelector('[data-course-empty]');
    var activeFilter = 'all';

    function readProgress() {
        try {
            return JSON.parse(localStorage.getItem(storageKey)) || {};
        } catch (error) {
            return {};
        }
    }

    function saveProgress(progress) {
        localStorage.setItem(storageKey, JSON.stringify(progress));
    }

    function getCourseProgress(progress, courseId) {
        if (!progress[courseId]) {
            progress[courseId] = {};
        }

        return progress[courseId];
    }

    function countCompleted(courseProgress) {
        return Object.keys(courseProgress).filter(function (itemId) {
            return courseProgress[itemId] === 'complete';
        }).length;
    }

    function setItemStatus(item, status) {
        var isComplete = status === 'complete';
        var button = item.querySelector('[data-status-toggle]');

        item.dataset.status = status;
        item.classList.toggle('is-complete', isComplete);

        if (button) {
            button.textContent = isComplete ? 'Ukończone' : 'Do zrobienia';
            button.setAttribute('aria-pressed', String(isComplete));
        }
    }

    function updateCourseSummary(items) {
        if (!course) {
            return;
        }

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

    function updateCourseCards(progress) {
        courseCards.forEach(function (card) {
            var courseId = card.dataset.courseCard;
            var savedCourse = progress[courseId] || {};
            var completed = countCompleted(savedCourse);
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

            card.dataset.completed = String(completed);
            card.dataset.total = String(total);
            card.dataset.progressPercent = String(percent);

            if (total > 0 && completed === total) {
                card.dataset.courseState = 'complete';
            } else if (completed > 0) {
                card.dataset.courseState = 'in-progress';
            } else {
                card.dataset.courseState = 'todo';
            }
        });
    }

    function updateFilterButtons() {
        filterButtons.forEach(function (button) {
            var isActive = button.dataset.courseFilter === activeFilter;

            button.classList.toggle('tab-active', isActive);
            button.classList.toggle('text-slate-500', !isActive);
            button.classList.toggle('hover:text-slate-300', !isActive);
        });
    }

    function applyCourseFilter() {
        var currentProgress = readProgress();
        var visibleCount = 0;

        updateCourseCards(currentProgress);

        courseCards.forEach(function (card) {
            var courseId = card.dataset.courseCard;
            var savedCourse = currentProgress[courseId] || {};
            var completed = countCompleted(savedCourse);
            var total = Number(card.dataset.courseTotal) || 0;
            var isInProgress = completed > 0 && completed < total;
            var isComplete = total > 0 && completed === total;
            var shouldShow = activeFilter === 'all'
                || (activeFilter === 'in-progress' && isInProgress)
                || (activeFilter === 'complete' && isComplete);

            card.classList.toggle('course-card-hidden', !shouldShow);
            card.hidden = !shouldShow;
            card.style.display = shouldShow ? '' : 'none';

            if (shouldShow) {
                visibleCount += 1;
            }
        });

        if (emptyState) {
            emptyState.hidden = visibleCount > 0;
        }

        updateFilterButtons();
    }

    var progress = readProgress();

    updateCourseCards(progress);
    applyCourseFilter();

    if (filterContainer) {
        filterContainer.addEventListener('click', function (event) {
            var button = event.target.closest('[data-course-filter]');

            if (!button) {
                return;
            }

            activeFilter = button.dataset.courseFilter || 'all';
            applyCourseFilter();
        });
    }

    if (!course) {
        return;
    }

    var courseId = course.dataset.progressCourse;
    var courseProgress = getCourseProgress(progress, courseId);
    var items = Array.prototype.slice.call(course.querySelectorAll('[data-progress-item]'));

    items.forEach(function (item) {
        var itemId = item.dataset.progressItem;
        var savedStatus = courseProgress[itemId] || 'todo';
        var button = item.querySelector('[data-status-toggle]');

        setItemStatus(item, savedStatus);

        if (button) {
            button.addEventListener('click', function () {
                var nextStatus = item.dataset.status === 'complete' ? 'todo' : 'complete';

                courseProgress[itemId] = nextStatus;
                progress[courseId] = courseProgress;

                saveProgress(progress);
                setItemStatus(item, nextStatus);
                updateCourseSummary(items);
                updateCourseCards(progress);
                applyCourseFilter();
            });
        }
    });

    updateCourseSummary(items);
}());
