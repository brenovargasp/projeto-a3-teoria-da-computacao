document.addEventListener("DOMContentLoaded", () => {
    const floorMap = ["T", "1", "2", "3"];

    const catImages = {
        T: "img/quest.png",
        1: "img/andar1.png",
        2: "img/andar2.png",
        3: "img/andar3.png"
    };

    let currentFloorIndex = 0;
    let isMoving = false;

    const displaySpan = document.getElementById("floor-display");
    const directionIcon = document.getElementById("direction-icon");
    const cat = document.getElementById("cat");
    const doorLeft = document.getElementById("door-left");
    const doorRight = document.getElementById("door-right");
    const buttons = document.querySelectorAll(".floor-btn");

    buttons.forEach((button) => {
        button.addEventListener("click", (event) => {
            const targetFloor = event.currentTarget.getAttribute("data-floor");
            requestFloor(targetFloor, event.currentTarget);
        });
    });

    async function requestFloor(targetFloorString, buttonElement) {
        if (isMoving) return;

        const targetIndex = floorMap.indexOf(targetFloorString);
        if (targetIndex === currentFloorIndex) return;

        isMoving = true;
        setButtonsState(true);
        buttonElement.classList.add("active");

        const goingUp = currentFloorIndex < targetIndex;
        directionIcon.src = goingUp ? "img/subindo.png" : "img/descendo.png";
        directionIcon.style.display = "block";

        await closeDoors();
        await moveElevator(targetIndex);
        await openDoors();

        directionIcon.removeAttribute("src");
        directionIcon.style.display = "none";

        buttonElement.classList.remove("active");
        setButtonsState(false);
        isMoving = false;
    }

    function setButtonsState(disabled) {
        buttons.forEach((button) => {
            button.disabled = disabled;
        });
    }

    function closeDoors() {
        return new Promise((resolve) => {
            doorLeft.classList.remove("open");
            doorRight.classList.remove("open");
            setTimeout(resolve, 1000);
        });
    }

    function openDoors() {
        return new Promise((resolve) => {
            doorLeft.classList.add("open");
            doorRight.classList.add("open");
            setTimeout(resolve, 1000);
        });
    }

    function moveElevator(targetIndex) {
        return new Promise((resolve) => {
            const step = currentFloorIndex < targetIndex ? 1 : -1;

            function changeFloor() {
                if (currentFloorIndex !== targetIndex) {
                    currentFloorIndex += step;

                    const currentFloor = floorMap[currentFloorIndex];
                    displaySpan.innerText = currentFloor;

                    cat.style.transform = "scale(0.92)";
                    cat.style.opacity = "0";

                    setTimeout(() => {
                        cat.src = catImages[currentFloor];
                        cat.style.transform = "scale(1)";
                        cat.style.opacity = "1";
                    }, 180);

                    setTimeout(changeFloor, 1100);
                } else {
                    resolve();
                }
            }

            setTimeout(changeFloor, 450);
        });
    }
});