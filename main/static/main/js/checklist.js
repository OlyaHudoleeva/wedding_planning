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

$(document).ready(function () {
    $(".form-check-input").change(function () {
        if (this.checked) {
            $.post(
                "handle_task",
                {
                    'status': 'C',
                    'id': $(this).data("id")
                }
            )
        }
        // else
    });
});

// document.getElementById("add-task-list-btn").addEventListener("click", function () {
//     let task_group_name = document.getElementById("task-list-name").value;
//
//     let new_card = document.createElement("div");
//     new_card.className = "card";
//
// })

