var parser = require("@babel/parser");
var traverse = require("@babel/traverse").default;
var t = require("@babel/types");
var generator = require("@babel/generator").default

function template(jscode){
    return parser.parse(jscode).program.body[0]
}

var global_seed = 123
var global_random = (function(seed){return function(){return seed = (seed * 9301 + 49297) % 233280, seed / 233280.0}})(global_seed)

Array.prototype.random_sort = function(){
    for (var i = 0; i < this.length; i++) {
        var temp = this[i]
        var nidx = global_random()*this.length ^ 0
        this[i] = this[nidx]
        this[nidx] = temp
    }
    return this
}

function hoist_var(path){
    if (path.node.kind !== 'var' || 
        t.isForOfStatement(path.parentPath.node) || 
        t.isForInStatement(path.parentPath.node)){
        return
    }
    var root = (path.getFunctionParent() || path.findParent(function(e){return t.isProgram(e)})).node
    var vars = root.vars = root.vars || []
    var node = path.node
    var keep = []
    function add_vars(node){
        if (t.isIdentifier(node)){
            if (vars.indexOf(node.name) == -1){
                vars.push(node.name)
            }
        }else if (t.isArrayPattern(node)){
            var eles = node.elements
            for (var j = 0; j < eles.length; j++) {
                add_vars(eles[j])
            }
        }else if (t.isRestElement(node)){
            add_vars(node.argument)
        }else if (t.isObjectPattern(node)){
            var props = node.properties
            for (var j = 0; j < props.length; j++) {
                add_vars(props[j].value)
            }
        }else if (node == null){
            return
        }else{
            throw Error('unknown decl type.' + node && node.type)
        }
    }
    for (var i = 0; i < node.declarations.length; i++) {
        if (node.declarations[i].init){
            keep.push(t.ExpressionStatement(t.AssignmentExpression('=', node.declarations[i].id, node.declarations[i].init)))
        }
        add_vars(node.declarations[i].id)
    }
    if (keep.length){
        path.replaceWithMultiple(keep)
    }else{
        path.remove()
    }
}
function add_hoist_var(path){
    var node = path.node
    var vars = node.vars
    if (vars && vars.length){
        if(!node.body){
            throw Error('no body.')
        }
        var body = Array.isArray(node.body) ? node.body : node.body.body
        var _vars = []
        for (var i = 0; i < vars.length; i++) {
            _vars.push(t.VariableDeclarator(t.Identifier(vars[i])))
        }
        body.unshift(t.VariableDeclaration('var', _vars))
    }
}

function v_ctl_flow(path){
    var _body = path.node.body.body
    var _indx = Array(_body.length)
                    .fill(0)
                    .map(function(_, idx){return idx})
                    .random_sort()
    // 请确保这两个额外的变量和其他正常代码的变量不冲突
    var switch_name = 'cilame_switch'
    var switch_indx = 'cilame_indexer'
    var init = template(`var ${switch_name} = "${_indx.join('|')}".split("|"), ${switch_indx} = 0`)
    var whiles = template(`while(1){
        switch(${switch_name}[${switch_indx}++]){}
        break
    }`)
    var _cases = []
    for (var i = 0; i < _body.length; i++) {
        var cs = t.SwitchCase(t.StringLiteral(''+_indx[i]), [_body[i], t.ContinueStatement()])
        _cases.push(cs)
    }
    whiles.body.body[0].cases = _cases.random_sort()
    path.node.body = t.BlockStatement([
        init,
        whiles
    ])
}

function multi_process_ob(jscode){
    var ast = parser.parse(jscode)
    traverse(ast, {'VariableDeclaration': hoist_var})
    traverse(ast, {'Function|Program': add_hoist_var})
    traverse(ast, {'VariableDeclaration': add_hoist_var})
    traverse(ast, {'FunctionDeclaration|FunctionExpression': v_ctl_flow})
    return generator(ast).code
}

const fs = require('fs');
var jscode = fs.readFileSync("./source.js", {
    encoding: "utf-8"
});

code = multi_process_ob(jscode)
// console.log(code);
fs.writeFileSync('./code.js', code, {
    encoding: "utf-8"
})