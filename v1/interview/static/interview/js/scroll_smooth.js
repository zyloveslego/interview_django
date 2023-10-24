// <!--When a side Nav Bar item is clicked, the JavaScript event listener adds
// the class active to the clicked menu item and uses the scrollIntoView method
// to smoothly scroll to the corresponding content section. The CSS then changes
// the color of the active menu item using the .active class. -->

const menuItems = document.querySelectorAll('.menu-item');
const contentSections = document.querySelectorAll('.content-section');

function updateActiveMenuItem() {
    contentSections.forEach((section, index) => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= 200 && rect.bottom >= 200) {
            menuItems.forEach(item => item.classList.remove('active'));
            menuItems[index].classList.add('active');
        }
    });
}

// Event listener for scrolling
window.addEventListener('scroll', updateActiveMenuItem);

// Event listeners for menu items to scroll to the respective sections
menuItems.forEach((menuItem, index) => {
    menuItem.addEventListener('click', () => {
        contentSections[index].scrollIntoView({behavior: 'smooth'});
    });
});
