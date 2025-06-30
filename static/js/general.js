  document.addEventListener('DOMContentLoaded', () => {
  	const alertContainer = document.getElementById('alertContainer');
  	if (alertContainer && alertContainer.children.length > 0) {
  		setTimeout(() => {
  			alertContainer.innerHTML = '';
  		}, 3000);
  	}
  });
  document.addEventListener("DOMContentLoaded", () => {
  	const timezoneField = document.getElementById("timezone");
  	if (timezoneField) {
  		timezoneField.value = Intl.DateTimeFormat().resolvedOptions().timeZone;
  	}
  });