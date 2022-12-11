// 特殊调试代码










// (1)
// run in comment:  console.log(123) //... 







// (2)
// 需要确定代码没有主动获取 Object 原型链上的 splice 属性才可以使用
if(Object.defineProperties){
  Object.defineProperties(Object.prototype, {
    splice:{
      get: function(){
        console.log('Object splice')
      },
      configurable: true
    }
  })
}
// 当作为注入代码时候需要记得在进入用户代码时删除原型链上的该属性。
// delete Object.prototype.splice







// (3)
Error.prepareStackTrace = function(error, stack){
  if (!stack.length){
    console.log('prepareStackTrace.')
  }
};
console.log(new Error())







// (4)
if(Object.defineProperties){
  var emsg = Object.defineProperties(new Error, {
    message: {
      get: function(){
        console.log('Error message.')
      }
    },
    toString: {
      value: undefined,
    },
  })
  console.log(emsg);
}