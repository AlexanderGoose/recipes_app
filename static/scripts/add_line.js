document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('add_new_ing_line_container');
    var addButton = document.getElementById('add_new_ing_line_button');
    const LIMIT = 20;

    addButton.addEventListener("click", (e)=>{
        if (container.childElementCount < LIMIT)
        {
            // prevent form from submitting automatically
            e.preventDefault();

            //create a wrapper
            const wrapper = document.getElementById('add_new_ing_line_container');
        
            //create a new input
            const newInput = document.createElement('input');
            newInput.type = 'text';
            newInput.classList.add('ingredient');
            newInput.name = 'ingredient';
            newInput.placeholder = "Enter new item..."
        
            wrapper.appendChild(newInput);
        }
        else
        {
            alert('Max number of ingredients have been added!');
        }
    })
})
  

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('add_new_instr_line_container');
    var addInstrButton = document.getElementById('add_new_instr_line_button');
    const LIMIT = 10;

    addInstrButton.addEventListener("click", (e)=>{
        if (container.childElementCount < LIMIT)
        {
            // prevent form from submitting automatically
            e.preventDefault();

            //create a wrapper
            const wrapper = document.getElementById('add_new_instr_line_container');
        
            //create a new input
            const newInput = document.createElement('input');
            newInput.type = 'text';
            newInput.classList.add('instruction');
            newInput.name = 'instruction';
            newInput.placeholder = "Enter new item..."
        
            wrapper.appendChild(newInput);
        }
        else
        {
            alert('Max number of instructions have been added!');
        }
    })
})