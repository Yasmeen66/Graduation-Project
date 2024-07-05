function openSelectedTab() {
    var selectedTabOption = document.querySelector('input[name="inlineRadioOptions"]:checked');
    if (selectedTabOption) {
        var tabValue = selectedTabOption.value;
        var newTab = window.open('', '_blank');
        // Open different URLs based on the selected radio option
        switch (tabValue) {
            case 'option1':
                newTab.location.href = 'https://example.com/option1';
                break;
            case 'option2':
                newTab.location.href = 'https://example.com/option2';
                break;
            case 'option3':
                newTab.location.href = 'https://example.com/option3';
                break;
            case 'option4':
                newTab.location.href = 'https://example.com/option4';
                break;
            // Add more cases as needed
            default:
                break;
        }
    } else {
        alert('Please select a tab option.');
    }
}
function myFunction() {
    // Declare variables
    var input, filter, ul, li, a, i;
    input = document.getElementById("mySearch");
    filter = input.value.toUpperCase();
    ul = document.getElementById("myMenu");
    li = ul.getElementsByTagName("li");

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}