document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".tab-wizard2");
  const submitButton = document.querySelector(".actions a[href='#finish']");

  if (submitButton) {
    submitButton.addEventListener("click", function (event) {
      event.preventDefault();
      form.submit();
    });
  }
});
