// npm install jsdom --save
const { JSDOM } = require("jsdom");

const jsdom = new JSDOM('<!doctype html><html><body></body></html>')
const {window} = jsdom;
Object.keys(window).forEach(property =>{
    try{
        if (typeof global[property] == 'undefined'){
            global[property] = window[property]
        }
    }catch(e){
        // console.log(e)
    }
})