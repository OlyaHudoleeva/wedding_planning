function toggleAccordion(textId, buttonId) {
    const text = document.getElementById(textId);
    const button = document.getElementById(buttonId);
    const isAreaExpanded = button.ariaExpanded == "true";
    if (isAreaExpanded) {
        text.classList.remove("show");
        button.classList.add("collapsed");
        button.ariaExpanded = "false";
    } else {
        text.classList.add("show");
        button.classList.remove("collapsed");
        button.ariaExpanded = "true";
    }

}