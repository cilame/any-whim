function getIPs(callback) {
    var ip_dups = {};
    var RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
    if (!RTCPeerConnection) {
        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        var win = iframe.contentWindow;
        window.RTCPeerConnection = win.RTCPeerConnection;
        window.mozRTCPeerConnection = win.mozRTCPeerConnection;
        window.webkitRTCPeerConnection = win.webkitRTCPeerConnection;
        RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
    }
    if(!RTCPeerConnection){
        (console.warn || console.log)('not support RTC')
        return
    }
    var mediaConstraints = {
        optional: [{
            RtpDataChannels: true
        }]
    };
    var servers = {
        iceServers: [{ urls: [
            "stun:stun.l.google.com:19302?transport=udp", 
            "stun:stun1.l.google.com:19302?transport=udp", 
            "stun:stun2.l.google.com:19302?transport=udp", 
            "stun:stun3.l.google.com:19302?transport=udp", 
            "stun:stun4.l.google.com:19302?transport=udp", 
            "stun:stun.ekiga.net?transport=udp", 
            "stun:stun.ideasip.com?transport=udp", 
            "stun:stun.rixtelecom.se?transport=udp", 
            "stun:stun.schlund.de?transport=udp", 
            "stun:stun.stunprotocol.org:3478?transport=udp", 
            "stun:stun.voiparound.com?transport=udp", 
            "stun:stun.voipbuster.com?transport=udp", 
            "stun:stun.voipstunt.com?transport=udp", 
            "stun:stun.voxgratia.org?transport=udp", 
            "stun:stun.1und1.de:3478?transport=udp", 
            "stun:stun.gmx.net:3478?transport=udp", 
            "stun:23.21.150.121:3478?transport=udp", 
            "stun:iphone-stun.strato-iphone.de:3478?transport=udp", 
            "stun:numb.viagenie.ca:3478?transport=udp", 
            "stun:stun.12connect.com:3478?transport=udp", 
            "stun:stun.12voip.com:3478?transport=udp", 
            "stun:stun.1und1.de:3478?transport=udp", 
            "stun:stun.2talk.co.nz:3478?transport=udp", 
            "stun:stun.2talk.com:3478?transport=udp", 
            "stun:stun.3cx.com:3478?transport=udp", 
            "stun:stun.aa.net.uk:3478?transport=udp", 
            "stun:stun.acrobits.cz:3478?transport=udp", 
            "stun:stun.actionvoip.com:3478?transport=udp", 
            "stun:stun.advfn.com:3478?transport=udp", 
            "stun:stun.aeta-audio.com:3478?transport=udp", 
            "stun:stun.aeta.com:3478?transport=udp", 
            "stun:stun.altar.com.pl:3478?transport=udp", 
            "stun:stun.annatel.net:3478?transport=udp", 
            "stun:stun.antisip.com:3478?transport=udp", 
            "stun:stun.arbuz.ru:3478?transport=udp", 
            "stun:stun.avigora.fr:3478?transport=udp", 
            "stun:stun.awa-shima.com:3478?transport=udp", 
            "stun:stun.b2b2c.ca:3478?transport=udp", 
            "stun:stun.bahnhof.net:3478?transport=udp", 
            "stun:stun.barracuda.com:3478?transport=udp", 
            "stun:stun.bluesip.net:3478?transport=udp", 
            "stun:stun.bmwgs.cz:3478?transport=udp", 
            "stun:stun.budgetsip.com:3478?transport=udp", 
            "stun:stun.cablenet-as.net:3478?transport=udp", 
            "stun:stun.callromania.ro:3478?transport=udp", 
            "stun:stun.callwithus.com:3478?transport=udp", 
            "stun:stun.cheapvoip.com:3478?transport=udp", 
            "stun:stun.ciktel.com:3478?transport=udp", 
            "stun:stun.cloopen.com:3478?transport=udp", 
            "stun:stun.comfi.com:3478?transport=udp", 
            "stun:stun.commpeak.com:3478?transport=udp", 
            "stun:stun.comtube.com:3478?transport=udp", 
            "stun:stun.comtube.ru:3478?transport=udp", 
            "stun:stun.cope.es:3478?transport=udp", 
            "stun:stun.counterpath.com:3478?transport=udp", 
            "stun:stun.counterpath.net:3478?transport=udp", 
            "stun:stun.dcalling.de:3478?transport=udp", 
            "stun:stun.demos.ru:3478?transport=udp", 
            "stun:stun.develz.org:3478?transport=udp", 
            "stun:stun.dingaling.ca:3478?transport=udp", 
            "stun:stun.doublerobotics.com:3478?transport=udp", 
            "stun:stun.dus.net:3478?transport=udp", 
            "stun:stun.easycall.pl:3478?transport=udp", 
            "stun:stun.easyvoip.com:3478?transport=udp", 
            "stun:stun.ekiga.net:3478?transport=udp", 
            "stun:stun.epygi.com:3478?transport=udp", 
            "stun:stun.etoilediese.fr:3478?transport=udp", 
            "stun:stun.faktortel.com.au:3478?transport=udp", 
            "stun:stun.freecall.com:3478?transport=udp", 
            "stun:stun.freeswitch.org:3478?transport=udp", 
            "stun:stun.freevoipdeal.com:3478?transport=udp", 
            "stun:stun.gmx.de:3478?transport=udp", 
            "stun:stun.gmx.net:3478?transport=udp", 
            "stun:stun.gradwell.com:3478?transport=udp", 
            "stun:stun.halonet.pl:3478?transport=udp", 
            "stun:stun.hellonanu.com:3478?transport=udp", 
            "stun:stun.hoiio.com:3478?transport=udp", 
            "stun:stun.hosteurope.de:3478?transport=udp", 
            "stun:stun.ideasip.com:3478?transport=udp", 
            "stun:stun.infra.net:3478?transport=udp", 
            "stun:stun.internetcalls.com:3478?transport=udp", 
            "stun:stun.intervoip.com:3478?transport=udp", 
            "stun:stun.ipcomms.net:3478?transport=udp", 
            "stun:stun.ipfire.org:3478?transport=udp", 
            "stun:stun.ippi.fr:3478?transport=udp", 
            "stun:stun.ipshka.com:3478?transport=udp", 
            "stun:stun.irian.at:3478?transport=udp", 
            "stun:stun.it1.hr:3478?transport=udp", 
            "stun:stun.ivao.aero:3478?transport=udp", 
            "stun:stun.jumblo.com:3478?transport=udp", 
            "stun:stun.justvoip.com:3478?transport=udp", 
            "stun:stun.kanet.ru:3478?transport=udp", 
            "stun:stun.kiwilink.co.nz:3478?transport=udp", 
            "stun:stun.linea7.net:3478?transport=udp", 
            "stun:stun.linphone.org:3478?transport=udp", 
            "stun:stun.liveo.fr:3478?transport=udp", 
            "stun:stun.lowratevoip.com:3478?transport=udp", 
            "stun:stun.lugosoft.com:3478?transport=udp", 
            "stun:stun.lundimatin.fr:3478?transport=udp", 
            "stun:stun.magnet.ie:3478?transport=udp", 
            "stun:stun.mgn.ru:3478?transport=udp", 
            "stun:stun.mit.de:3478?transport=udp", 
            "stun:stun.mitake.com.tw:3478?transport=udp", 
            "stun:stun.miwifi.com:3478?transport=udp", 
            "stun:stun.modulus.gr:3478?transport=udp", 
            "stun:stun.myvoiptraffic.com:3478?transport=udp", 
            "stun:stun.mywatson.it:3478?transport=udp", 
            "stun:stun.nas.net:3478?transport=udp", 
            "stun:stun.neotel.co.za:3478?transport=udp", 
            "stun:stun.netappel.com:3478?transport=udp", 
            "stun:stun.netgsm.com.tr:3478?transport=udp", 
            "stun:stun.nfon.net:3478?transport=udp", 
            "stun:stun.noblogs.org:3478?transport=udp", 
            "stun:stun.noc.ams-ix.net:3478?transport=udp", 
            "stun:stun.nonoh.net:3478?transport=udp", 
            "stun:stun.nottingham.ac.uk:3478?transport=udp", 
            "stun:stun.nova.is:3478?transport=udp", 
            "stun:stun.on.net.mk:3478?transport=udp", 
            "stun:stun.ooma.com:3478?transport=udp", 
            "stun:stun.ooonet.ru:3478?transport=udp", 
            "stun:stun.oriontelekom.rs:3478?transport=udp", 
            "stun:stun.ozekiphone.com:3478?transport=udp", 
            "stun:stun.phone.com:3478?transport=udp", 
            "stun:stun.pjsip.org:3478?transport=udp", 
            "stun:stun.poivy.com:3478?transport=udp", 
            "stun:stun.powerpbx.org:3478?transport=udp", 
            "stun:stun.powervoip.com:3478?transport=udp", 
            "stun:stun.ppdi.com:3478?transport=udp", 
            "stun:stun.qq.com:3478?transport=udp", 
            "stun:stun.rackco.com:3478?transport=udp", 
            "stun:stun.rapidnet.de:3478?transport=udp", 
            "stun:stun.rb-net.com:3478?transport=udp", 
            "stun:stun.rixtelecom.se:3478?transport=udp", 
            "stun:stun.rockenstein.de:3478?transport=udp", 
            "stun:stun.rolmail.net:3478?transport=udp", 
            "stun:stun.rynga.com:3478?transport=udp", 
            "stun:stun.schlund.de:3478?transport=udp", 
            "stun:stun.sigmavoip.com:3478?transport=udp", 
            "stun:stun.sip.us:3478?transport=udp", 
            "stun:stun.sipdiscount.com:3478?transport=udp", 
            "stun:stun.sipgate.net:3478?transport=udp", 
            "stun:stun.siplogin.de:3478?transport=udp", 
            "stun:stun.sipnet.net:3478?transport=udp", 
            "stun:stun.sipnet.ru:3478?transport=udp", 
            "stun:stun.siportal.it:3478?transport=udp", 
            "stun:stun.sippeer.dk:3478?transport=udp", 
            "stun:stun.siptraffic.com:3478?transport=udp", 
            "stun:stun.skylink.ru:3478?transport=udp", 
            "stun:stun.sma.de:3478?transport=udp", 
            "stun:stun.smartvoip.com:3478?transport=udp", 
            "stun:stun.smsdiscount.com:3478?transport=udp", 
            "stun:stun.softjoys.com:3478?transport=udp", 
            "stun:stun.solcon.nl:3478?transport=udp", 
            "stun:stun.solnet.ch:3478?transport=udp", 
            "stun:stun.sonetel.com:3478?transport=udp", 
            "stun:stun.sonetel.net:3478?transport=udp", 
            "stun:stun.sovtest.ru:3478?transport=udp", 
            "stun:stun.speedy.com.ar:3478?transport=udp", 
            "stun:stun.srce.hr:3478?transport=udp", 
            "stun:stun.ssl7.net:3478?transport=udp", 
            "stun:stun.stunprotocol.org:3478?transport=udp", 
            "stun:stun.symplicity.com:3478?transport=udp", 
            "stun:stun.t-online.de:3478?transport=udp", 
            "stun:stun.tagan.ru:3478?transport=udp", 
            "stun:stun.teachercreated.com:3478?transport=udp", 
            "stun:stun.tel.lu:3478?transport=udp", 
            "stun:stun.telbo.com:3478?transport=udp", 
            "stun:stun.tng.de:3478?transport=udp", 
            "stun:stun.twt.it:3478?transport=udp", 
            "stun:stun.u-blox.com:3478?transport=udp", 
            "stun:stun.ucsb.edu:3478?transport=udp", 
            "stun:stun.uls.co.za:3478?transport=udp", 
            "stun:stun.unseen.is:3478?transport=udp", 
            "stun:stun.usfamily.net:3478?transport=udp", 
            "stun:stun.veoh.com:3478?transport=udp", 
            "stun:stun.vipgroup.net:3478?transport=udp", 
            "stun:stun.viva.gr:3478?transport=udp", 
            "stun:stun.vivox.com:3478?transport=udp", 
            "stun:stun.vline.com:3478?transport=udp", 
            "stun:stun.vo.lu:3478?transport=udp", 
            "stun:stun.vodafone.ro:3478?transport=udp", 
            "stun:stun.voicetrading.com:3478?transport=udp", 
            "stun:stun.voip.aebc.com:3478?transport=udp", 
            "stun:stun.voip.blackberry.com:3478?transport=udp", 
            "stun:stun.voip.eutelia.it:3478?transport=udp", 
            "stun:stun.voiparound.com:3478?transport=udp", 
            "stun:stun.voipblast.com:3478?transport=udp", 
            "stun:stun.voipbuster.com:3478?transport=udp", 
            "stun:stun.voipbusterpro.com:3478?transport=udp", 
            "stun:stun.voipcheap.co.uk:3478?transport=udp", 
            "stun:stun.voipcheap.com:3478?transport=udp", 
            "stun:stun.voipgain.com:3478?transport=udp", 
            "stun:stun.voipgate.com:3478?transport=udp", 
            "stun:stun.voipinfocenter.com:3478?transport=udp", 
            "stun:stun.voipplanet.nl:3478?transport=udp", 
            "stun:stun.voippro.com:3478?transport=udp", 
            "stun:stun.voipraider.com:3478?transport=udp", 
            "stun:stun.voipstunt.com:3478?transport=udp", 
            "stun:stun.voipwise.com:3478?transport=udp", 
            "stun:stun.voipzoom.com:3478?transport=udp", 
            "stun:stun.vopium.com:3478?transport=udp", 
            "stun:stun.voys.nl:3478?transport=udp", 
            "stun:stun.voztele.com:3478?transport=udp", 
            "stun:stun.webcalldirect.com:3478?transport=udp", 
            "stun:stun.wifirst.net:3478?transport=udp", 
            "stun:stun.wwdl.net:3478?transport=udp", 
            "stun:stun.xs4all.nl:3478?transport=udp", 
            "stun:stun.xtratelecom.es:3478?transport=udp", 
            "stun:stun.zadarma.com:3478?transport=udp", 
            "stun:stun.zadv.com:3478?transport=udp", 
            "stun:stun.zoiper.com:3478?transport=udp", 
            "stun:stun1.faktortel.com.au:3478?transport=udp", 
            "stun:stunserver.org:3478?transport=udp"
        ] }]
    }
    // var servers = { iceServers: [{ urls: "stun:stun.services.mozilla.com" }] };
    var pc = new RTCPeerConnection(servers,mediaConstraints);
    var ips = { ip_local: [], ipv4_public: [], ipv6_public: [] }
    function match_ip_with_string(str) {
        var ip_regex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/;
        var ip_addr = ip_regex.exec(str)[1];
        if (ip_dups[ip_addr] === undefined){
            if (ip_addr.match(/^(192\.168\.|169\.254\.|10\.|172\.(1[6-9]|2\d|3[01]))/)) {
                ips.ip_local.push(ip_addr)
            } else if (ip_addr.match(/^[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7}$/)) {
                ips.ipv6_public.push(ip_addr)
            } else {
                ips.ipv4_public.push(ip_addr)
            }
            console.log(ip_addr)
        }
        ip_dups[ip_addr] = true;
    }
    pc.onicecandidate = function(ice) {
        ice.candidate && match_ip_with_string(ice.candidate.candidate)
    }
    pc.createDataChannel("");
    pc.createOffer(function(result) {
        pc.setLocalDescription(result, function() {}, function() {});
    }, function() {});
}

getIPs();
