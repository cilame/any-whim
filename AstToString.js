const typeMap= {
    'File':function (node) {
        return [node.program];
    },
    'Program':function (node) {
        return [node.body]
    },
    'Block':function (node) {
        return [
            '/*',
            node.value,
            '*/'
        ]
    },
    'CommentBlock':function (node) {
        return [
            '/*',
            node.value,
            '*/'
        ]
    },
    'Line':function (node) {
        return [
            '//',
            node.value
        ]
    },
    'CommentLine':function (node) {
        return [
            '//',
            node.value
        ]
    },
    'VariableDeclaration':function (node) {
        return [
            node.kind+' ',
            node.declarations,
        ];
    },
    'VariableDeclarator':function (node) {
        if(node.init===null){
            return [
                node.id,
                ';'
            ];
        }
        return [
            node.id,
            '=',
            node.init,
            ';'
        ];
    },
    'Identifier':function (node) {
        return node.name;
    },
    'CallExpression':function (node) {
        return [
            node.callee,
            '(',
            joinSymbol(node.arguments,','),
            ')'
        ];
    },
    'FunctionDeclaration':function (node) {
        return [
            node.async?'async ':'',
            node.generator?'function* ':'function ',
            node.id,
            '(',
            joinSymbol(node.params,','),
            ')',
            node.body,
        ];

    },
    'BlockStatement':function (node) {
        return [
            '{',
            node.body,
            '}',
        ];
    },
    'ReturnStatement':function (node) {
        return [
            'return ',
            node.argument||'',
            ';'
        ]
    },
    'Literal':function (node) {
        return node.raw;
    },
    'ExpressionStatement':function (node) {
        return [
            node.expression,
            ';'
        ]
    },
    'Property':function (node) {
        if(node.kind==='get'||node.kind==='set'){
            return [
                node.kind+' ',
                node.key,
                AstToString(node.value).replace('function','')
            ];
        }
        if(node.method){
            return [
                node.value.async?'async ':'',
                node.key,
                AstToString(node.value).replace('function','')
            ];
        }
        if(node.shorthand){
            return [
                node.value
            ];
        }

        return [
            node.key,
            ':',
            node.value
        ];
    },
    'DirectiveLiteral':function (node) {},
    'Directive':function (node) {},

    'Decorator':function (node) {
        return [
            '@',
            node.expression
        ];
    },
    'BreakStatement':function (node) {
        return [
            'break',
            node.label?[' ',node.label]:'',
            ';'
        ]
    },
    'ContinueStatement':function (node) {
        return 'continue;'
    },
    'DebuggerStatement':function (node) {
        return 'debugger;'
    },
    'DoWhileStatement':function (node) {
        return [
            'do',
            node.body,
            'while(',
            node.test,
            ')'
        ];
    },

    'IfStatement':function (node) {
        return [
            'if(',
            node.test,
            ')',
            node.consequent,
            node.alternate?[node.alternate.type==='IfStatement'?'else ':'else',node.alternate]:'',

        ];
    },

    'SwitchCase':function (node) {
        return [
            node.test?[
                'case ',
                node.test,
                ':'
            ]:'default:',

            node.consequent
        ];
    },
    'SwitchStatement':function (node) {
        return [
            'switch (',
            node.discriminant,
            '){',
            node.cases,
            '}'
        ];
    },
    'ThrowStatement':function (node) {
        return [
            'throw ',
            node.argument,
            ';'
        ];
    },
    'CatchClause':function (node) {
        return [
            'catch(',
            node.param,
            ')',
            node.body
        ];
    },
    'TryStatement':function (node) {
        return [
            'try',
            node.block,
            node.handler,
            node.finalizer?'finally':'',
            node.finalizer||'',
        ];
    },
    'WhileStatement':function (node) {
        return [
            'while(',
            node.test,
            ')',
            node.body
        ];
    },
    'WithStatement':function (node) {},
    'EmptyStatement':function (node) {return '';},
    'LabeledStatement':function (node) {
        return [
            node.label,
            ':',
            node.body,
        ];
    },

    'ForStatement':function (node) {
        return [
            'for(',
            AstToString(node.init).replace(';',''),
            ';',
            node.test,
            ';',
            node.update,
            ')',
            node.body,
        ];
    },
    'ForInStatement':function (node) {
        return [
            'for(',
            AstToString(node.left).replace(';',''),
            ' in ',
            node.right,
            ')',
            node.body,
        ];
    },

    'FunctionExpression':function (node) {
        return [
            'function(',
            joinSymbol(node.params,','),
            ')',
            node.body,
        ]
    },
    'ClassDeclaration':function (node) {
        return [
            node.decorators,
            'class ',
            node.id,
            node.superClass===null?'':[' extends ',node.superClass],
            node.body,

        ]
    },
    'ClassExpression':function (node) {
        return [
            'class ',
            node.id,
            node.superClass?['extends ',node.superClass]:'',
            node.body,
        ]
    },
    'ClassBody':function (node) {
        return [
            '{',
            node.body,
            '}'
        ];
    },
    'ClassProperty':function (node) {
        return [
            node.static?'static ':'',
            node.key,
            '=',
            node.value,
            ';'
        ]
    },
    'ClassMethod':function (node) {
        return [
            node.decorators,
            node.static?'static ':'',
            node.async?'async ':'',
            node.key,
            '(',
            joinSymbol(node.params,','),
            ')',
            node.body
        ]
    },
    'ExportNamespaceSpecifier':function (node) {},
    'ExportAllDeclaration':function (node) {},
    'ExportDefaultSpecifier':function (node) {},
    'ExportDefaultDeclaration':function (node) {
        return [
            'export default ',
            node.declaration,
            ';'
        ]
    },
    'ExportNamedDeclaration':function (node) {
        return [
            'export ',
            node.specifiers?joinSymbol(node.specifiers):'',
            node.declaration||"",
            ';'
        ]
    },
    'ExportSpecifier':function (node) {
        return [
            '{',
            node.exported,
            '}'
        ];
    },
    'ImportDeclaration':function (node) {
        const arr1=[]
        const arr2=[]

        node.specifiers.forEach(function (item,i) {
            if(item.type==='ImportSpecifier'){
                arr2.push(item);
            }else{
                arr1.push(item);
            }
        })

        return [
            'import ',
            node.specifiers.length?[
                    arr1,
                    arr2.length?[arr1.length>0?',':'','{',joinSymbol(arr2,','),'}']:'',
                    ' from ',
                ]:'',
            node.source,
            ';'
        ];
    },
    'ImportNamespaceSpecifier':function (node) {
        return [
            '* as',
            node.local
        ];
    },
    'ImportSpecifier':function (node) {
        if(node.imported.name===node.local.name){
            return [
                node.imported,
            ];
        }
        return [
            node.imported,
            ' as ',
            node.local,
        ];
    },
    'ImportDefaultSpecifier':function (node) {
        return [node.local]
    },
    'SpreadElement':function (node) {
        return [
            '...',
            node.argument
        ]
    },
    'RestElement':function (node) {
        return ['...',node.argument];
    },
    'ArrayPattern':function (node) {
        return [
            '[',
            joinSymbol(node.elements,','),
            ']'
        ];
    },
    'AssignmentPattern':function (node) {
        return [
            node.left,
            '=',
            node.right
        ];
    },
    'SequenceExpression':function (node) {
        return [
            joinSymbol(node.expressions,',')
        ];
    },
    'AssignmentExpression':function (node) {
        return [
            node.left,
            node.operator,
            node.right,
        ]
    },
    'ConditionalExpression':function (node) {
        return [
            node.test,
            '?',
            node.consequent,
            ':',
            node.alternate
        ]
    },
    'LogicalExpression':function (node) {
        return [
            node.left,
            node.operator,
            node.right,
        ]
    },
    'BinaryExpression':function (node) {
        return [
            node.extra && node.extra.parenthesized?'(':'',
            node.left,
            node.operator,
            node.right,
            node.extra && node.extra.parenthesized?')':'',
        ]
    },
    'UpdateExpression':function (node) {
        if(node.prefix){
            return [
                node.operator,
                node.argument,
            ]
        }else{
            return [
                node.argument,
                node.operator,
            ]
        }

    },
    'UnaryExpression':function (node) {
        if(node.prefix){
            return [
                node.operator,
                node.argument,
            ]
        }
    },
    'BindExpression':function (node) {},
    'MemberExpression':function (node) {
        if(node.computed){
            return [
                node.object,
                '[',
                node.property,
                ']'
            ];
        }
        return [
            node.object,
            '.',
            node.property,
        ];
    },

    'TaggedTemplateExpression':function (node) {
        return [
            node.tag,
            node.quasi,
        ];
    },
    'Super':function (node) {
        return 'Super'
    },
    'Import':function (node) {},
    'ThisExpression':function (node) {
        return 'this';
    },
    'DoExpression':function (node) {
        return [
            'do',
            node.body
        ]
    },
    'NullLiteral':function (node) {
        return 'null';
    },
    'BooleanLiteral':function (node) {
        return ''+node.value;
    },
    'ArrayExpression':function (node) {
        return [
            '[',
            joinSymbol(node.elements,','),
            ']'
        ]
    },
    'StringLiteral':function (node) {
        return node.extra.raw;
    },
    'NumericLiteral':function (node) {
        return node.extra.raw;
    },
    'RegExpLiteral':function (node) {
        return node.extra.raw;
    },
    'MetaProperty':function (node) {},
    'NewExpression':function (node) {
        return [
            'new ',
            node.callee,
            '(',
            joinSymbol(node.arguments,','),
            ')'
        ];
    },
    'TemplateElement':function (node) {
        return node.value.raw;
    },
    'TemplateLiteral':function (node) {
        const arr=[]
        arr.push('`');
        node.expressions.forEach(function (item,i) {
            arr.push(node.quasis[i])
            arr.push(['${',item,'}'])
        })
        arr.push(node.quasis[node.expressions.length])
        arr.push('`');
        return arr;
    },
    'ObjectPattern':function (node) {
        return [
            '{',
            joinSymbol(node.properties,','),
            '}',
        ];
    },
    'ObjectExpression':function (node) {
        return [
            '{',
            joinSymbol(node.properties,','),
            '}',
        ];
    },
    'ObjectMethod':function (node) {
        return [
            node.async?'async ':'',
            node.key,
            '(',
            joinSymbol(node.params,','),
            ')',
            node.body,
        ];
    },
    'ObjectProperty':function (node) {
        if(node.shorthand){
            return [node.value];
        }
        return [
            node.key,
            ':',
            node.value
        ]
    },
    'ArrowFunctionExpression':function (node) {
        return [
            node.async?'async ':'',
            '(',
            joinSymbol(node.params,','),
            ')=>',
            node.body,
        ];
    },
    'AwaitExpression':function (node) {
        return [
            'await ',
            node.argument
        ];
    },
    'YieldExpression':function (node) {
        return [
            node.delegate?'yield* ':'yield ',
            node.argument
        ]
    },
    'MethodDefinition':function (node) {
        return [
            node.decorators,
            node.static?'static ':'',
            node.kind==='method'&&node.value.async?'async ':'',
            node.key,
            AstToString(node.value).replace('function','')
        ]
    },
    'DeclaredPredicate':function (node) {},
    'InferredPredicate':function (node) {},
    'DeclareClass':function (node) {},
    'TypeAnnotation':function (node) {},
    'DeclareFunction':function (node) {},
    'DeclareExportDeclaration':function (node) {},
    'DeclareVariable':function (node) {},
    'DeclareModule':function (node) {},
    'DeclareModuleExports':function (node) {},
    'DeclareTypeAlias':function (node) {},
    'DeclareOpaqueType':function (node) {},
    'DeclareInterface':function (node) {},
    'InterfaceExtends':function (node) {},
    'InterfaceDeclaration':function (node) {},
    'TypeAlias':function (node) {},
    'OpaqueType':function (node) {},
    'TypeParameterDeclaration':function (node) {},
    'TypeParameterInstantiation':function (node) {},
    'ObjectTypeIndexer':function (node) {},
    'ObjectTypeProperty':function (node) {},
    'ObjectTypeCallProperty':function (node) {},
    'ObjectTypeSpreadProperty':function (node) {},
    'ObjectTypeAnnotation':function (node) {},
    'QualifiedTypeIdentifier':function (node) {},
    'GenericTypeAnnotation':function (node) {},
    'TypeofTypeAnnotation':function (node) {},
    'TupleTypeAnnotation':function (node) {},
    'FunctionTypeParam':function (node) {},
    'AnyTypeAnnotation':function (node) {},
    'VoidTypeAnnotation':function (node) {},
    'BooleanTypeAnnotation':function (node) {},
    'MixedTypeAnnotation':function (node) {},
    'EmptyTypeAnnotation':function (node) {},
    'NumberTypeAnnotation':function (node) {},
    'StringTypeAnnotation':function (node) {},
    'FunctionTypeAnnotation':function (node) {},
    'StringLiteralTypeAnnotation':function (node) {},
    'BooleanLiteralTypeAnnotation':function (node) {},
    'NullLiteralTypeAnnotation':function (node) {},
    'NumericLiteralTypeAnnotation':function (node) {},
    'ThisTypeAnnotation':function (node) {},
    'ExistentialTypeParam':function (node) {},
    'ArrayTypeAnnotation':function (node) {},
    'NullableTypeAnnotation':function (node) {},
    'IntersectionTypeAnnotation':function (node) {},
    'UnionTypeAnnotation':function (node) {},
    'TypeCastExpression':function (node) {},
    'ClassImplements':function (node) {},
    'ExperimentalRestProperty':function (node) {
        return [
            '...',
            node.argument
        ]
    },


    'JSXEmptyExpression':function (node) {
        return '';
    },
    'JSXSpreadChild':function (node) {},
    'JSXExpressionContainer':function (node) {
        return [
            '{',
            node.expression,
            '}',
        ];
    },
    'JSXSpreadAttribute':function (node) {
        return [
            '{...',
            node.argument,
            '}'
        ];
    },
    'JSXAttribute':function (node) {
        return [
            node.name,
            '=',
            node.value,
        ];
    },
    'JSXIdentifier':function (node) {
        return node.name;
    },
    'JSXNamespacedName':function (node) {},
    'JSXMemberExpression':function (node) {},
    'JSXOpeningElement':function (node) {
        return [
            '<',
            node.name,
            node.attributes.length?[' ',joinSymbol(node.attributes,' ')]:'',
            node.selfClosing?' /':'',
            '>'
        ];
    },
    'JSXClosingElement':function (node) {
        return [
            '</',
            node.name,
            '>'
        ];
    },
    'JSXElement':function (node) {
        return [
            node.extra && node.extra.parenthesized?'(':'',
            node.openingElement,
            node.children,
            node.closingElement||'',
            node.extra && node.extra.parenthesized?')':'',
        ];
    },
}
//语法树转string
function AstChildToString(children) {
    let str='';
    children.forEach(function (node) {
        str+=AstToString(node)
    })
    return str;
}
//元素之间添加符号
function joinSymbol(oriArr,symbol,pre) {
    if(oriArr.length===0){return '';}
    const arr=[];
    if(pre){
        arr.push(pre)
    }
    oriArr.forEach(function (node,i) {
        arr.push(node);
        if(i<oriArr.length-1){
            arr.push(symbol);
        }
    })
    if(pre){
        arr.push(pre)
    }
    return arr;
}
//语法树转string
function AstToString(ast){
    if(Object.prototype.toString.call(ast)==='[object Array]'){
        return AstChildToString(ast);
    }else if(Object.prototype.toString.call(ast)==='[object String]'){
        return ast;
    }else if(ast===null){
        return '';
    }
    let code=typeMap[ast.type](ast);

    if(Object.prototype.toString.call(code)==='[object Array]'){
        const arr=code.map(function(obj){
            if(Object.prototype.toString.call(obj)==='[object Object]'){
                return AstToString(obj);
            }else if(Object.prototype.toString.call(obj)==='[object Array]'){
                return AstToString(obj);
            }
            return obj;
        })
        return arr.join('');
    }else{
        return code;
    }

}
module.exports=AstToString;