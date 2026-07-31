document.addEventListener('DOMContentLoaded', function () {
  const campusSelect = document.getElementById('id_campus');
  const deptSelect = document.getElementById('id_department');
  if (!campusSelect || !deptSelect) return;

  const allOptions = Array.from(deptSelect.options);

  function filterDepartments() {
    const campusId = campusSelect.value;
    deptSelect.innerHTML = '';
    allOptions.forEach((opt) => {
      if (!opt.value || !campusId || opt.dataset.campus === campusId) {
        deptSelect.appendChild(opt.cloneNode(true));
      }
    });
  }

  campusSelect.addEventListener('change', filterDepartments);
  filterDepartments(); // apply on page load too, e.g. when editing an existing user
});