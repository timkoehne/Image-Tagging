

var input = document.querySelector('input[name="tags"]'),
  // init Tagify script on the above inputs
  tagify = new Tagify(input, {
    whitelist: [],
    maxTags: 10,
    dropdown: {
      maxItems: 20,           // <- mixumum allowed rendered suggestions
      classname: "tags-look", // <- custom classname for this dropdown, so it could be targeted
      enabled: 0,             // <- show suggestions on focus
      closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
    }
  })

  loadPossibleTags()