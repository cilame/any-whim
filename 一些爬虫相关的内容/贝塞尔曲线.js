function make_trace(x1, y1, x2, y2){
  // 贝塞尔曲线
  function step_len(x1, y1, x2, y2){
    var ln = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return (ln / 10) ^ 0
  }
  var slen = step_len(x1, y1, x2, y2)
  if (slen < 3){
    return []
  }
  function factorial(x){
    for(var y = 1; x > 1;  x--) {
      y *= x
    }
    return y;
  }
  var lp = Math.random()
  var rp = Math.random()
  var xx1 = (x1 + (x2 - x1) / 12 * (4-lp*4)) ^ 0
  var yy1 = (y1 + (y2 - y1) / 12 * (8+lp*4)) ^ 0
  var xx2 = (x1 + (x2 - x1) / 12 * (8+rp*4)) ^ 0
  var yy2 = (y1 + (y2 - y1) / 12 * (4-rp*4)) ^ 0
  var points = [[x1, y1], [xx1, yy1], [xx2, yy2], [x2, y2]]
  var N = points.length
  var n = N - 1 
  var traces = []
  var step = slen
  for (var T = 0; T < step+1; T++) {
    var t = T*(1/step)
    var x = 0
    var y = 0
    for (var i = 0; i < N; i++) {
      var B = factorial(n)*t**i*(1-t)**(n-i)/(factorial(i)*factorial(n-i))
      x += points[i][0]*B
      y += points[i][1]*B
    }
    traces.push([x^0, y^0])
  }
  return traces
}

console.log(make_trace(123,123,333,333))