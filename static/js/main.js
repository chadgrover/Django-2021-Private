// Get search form and page links
let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");

// Make sure search form exists
if (searchForm) {
  for (let i = 0; i < pageLinks.length; i++) {
    let currentLink = pageLinks[i];
    currentLink.addEventListener("click", function (event) {
      // Stop whatever the default behavior is
      event.preventDefault();

      // Get the data page attribute using the this keyword
      let page = this.dataset.page;

      searchForm.innerHTML += `<input value=${page} name="page" hidden />`;

      searchForm.submit();
    });
  }
}
