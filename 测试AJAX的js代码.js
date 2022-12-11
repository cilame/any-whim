var url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=';
var headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
var body = {
    "params": "xy8WrM2VIoCcZy6cgHvbL9/CdVznwKAx68VdbqL+tss3O01ZuKlIpNzVvx/kgOWFWNbCxmKnlCMH4ZzgVv4ge+LTDK+PZ5uiNYIZ0F5eGJPAUINF54h5ScG+EIGBs8gC5uc0o25WVp6168KbU+C2DtuhnrGSGd/NOdpmkAuG7BNPRrGMSbddEtFBDcAzj5IW/C61siG/AUY2AXHwAWVJq2e1PFZddwhtYh09vFTMU3VuENk2Bvb0/3raNytl1kboXxwb+/One4We4lOkYAIhx/nLXn+79ZjjRSeLOQwWt+w=",
    "encSecKey": "1a20f023b02613b4a3160c3f03b6fa89db74021682afdfd446e2e99dfabf93887a402428a9f54585bb0cfae0bb19e24ab03496bc6269f453de3838419758ee29b63bd67437e62df1d52791e4c199c321cf908a6ce6f754d0819c80d9a428133d7cefa7831a7664e54324ef03509ddabb6818f6e91af8379f21acf8d77babc81d"
}

function cback(){
    // 将返回的结果直接写到 body 里面展示
    document.body.innerText = xml.response
}

function POST(url, headers, body){
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = cback;
    xml.open('POST', url, true);
    Object.keys(headers).map((eachKey)=>{
        xml.setRequestHeader(eachKey, headers[eachKey]);
    })
    xml.send(Object.keys(body).map((eachKey)=>{
        return encodeURIComponent(eachKey) + '=' + encodeURIComponent(body[eachKey]);
    }).join('&'));
    return xml;
}

function GET(url, headers){
    var xml = new XMLHttpRequest();
    xml.onreadystatechange = cback;
    xml.open('GET', url, true);
    Object.keys(headers).map((eachKey)=>{
        xml.setRequestHeader(eachKey, headers[eachKey]);
    })
    xml.send(null);
    return xml;
}

var xml = POST(url, headers, body);

