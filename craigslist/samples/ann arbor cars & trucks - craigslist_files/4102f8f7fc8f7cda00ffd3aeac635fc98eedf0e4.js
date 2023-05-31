/*****COPYRIGHTS

Copyright (c) 1995-2020, craigslist, Inc.

*****/
var cl=window.cl={showUnsupportedMessage:function(){document.body.className="show-curtain opaque unsupported-browser message";var e="craigslist",t="";try{e=document.querySelectorAll("head title")[0].innerText,t=document.querySelectorAll('meta[name="description"]')[0].content}catch(e){}document.getElementById("curtainText").innerHTML="<h1>"+e+"</h1><p>"+t+"</p><p>"+cl.specialCurtainMessages.unsupportedBrowser.join("</p><p>")+"</p>",cl.beacon("unsupported-"+(cl.unsupportedBrowser||"unsupported-browser"))},showUnrecoverableMessage:function(e,t){document.getElementById("curtainText").innerHTML="<h1>craigslist</h1><p>"+cl.specialCurtainMessages.unrecoverableError.join("</p><p>")+"</p>",document.body.className="show-curtain opaque unrecoverable message",e&&cl.beacon("unrecoverable-"+e),t&&cl.unexpected(t)},beacon:function(){var e=[];function t(e){var t,o=document.createElement("iframe");cl.devRoot||(o.onload=function(){document.body.removeChild(o)});try{t=window.location.origin}catch(e){}t||(t="https://"+(cl.devKnobs&&cl.devKnobs.sandboxUser||"")+"www.craigslist.org"),o.src=t+"/jslog?beacon="+encodeURIComponent(e),document.body.appendChild(o)}return function(o){try{if("start"===o){for(var n=0;n<e.length;n++)t(e[n]);e=0}else e?e.push(o):t(o)}catch(e){}}}(),jsonpCache:{},jsonp:function(e,t){cl.jsonpCache[e]=t}};window.onload=function(){cl.showUnsupportedMessage(),cl.beacon("start")},cl.init_=function(staticRoot,devRoot,siteName,resourceSetName,pageVars,devKnobs){cl.bootVersion={major:1,minor:1,patch:0},cl.staticRoot=staticRoot,cl.devRoot=devRoot,cl.siteName=siteName,cl.resourceSetName=resourceSetName||"",cl.pageVars=pageVars||{},cl.devKnobs=devKnobs||{},cl.sandbox=cl.devKnobs.sandboxUser=cl.devKnobs.sandboxUser||"";var doc=document,featureFail=0;try{if(window.addEventListener)if(JSON&&"x"===JSON.parse(JSON.stringify("x")))if(Uint8Array){var p=document.createElement("p");""!==p.style.flex&&""!==p.style["-webkit-flex"]&&(featureFail="no-flexbox"),p.classList.add("test"),p.classList.contains("test")||(featureFail="no-classList")}else featureFail="no-uint8-array";else featureFail="no-JSON";else featureFail="no-add-event-listener"}catch(e){featureFail="browser-sniff-error:"+e}if(cl.unsupportedBrowser=featureFail,!featureFail){doc.addEventListener("DOMContentLoaded",(function(){removeNode(doc.getElementById("no-js")),doc.body.classList.remove("no-js")})),cl.collectBfpForLogId={},CLError.prototype.toString=function(){return this.msg},cl.CLError=CLError,cl.clError=clError;var TextEncoderPolyfill=cl.TextEncoderPolyfill=function(){},globalErrorToError=cl.globalErrorToError=function(e,t){try{e||(e=new Error("globalErrorToError-missing-argument"));var o=new Error(t+":"+(e.type||"no-type")+":"+(e.message||"no-message")+(e.error?":"+e.error:"")),n="no-location";return e.filename&&(n=e.filename+":"+("lineno"in e?e.lineno:"?")+":"+("colno"in e?e.colno:"?")),e.error&&e.error.stack&&(n=n+"\n"+e.error.stack),o.filename=e.filename,o.lineno=e.lineno,o.colno=e.colno,o.stack=n,o.useless=!e.message&&!e.filename&&!e.error,o}catch(e){return bootError("globalErrorToError-exception",e)}};TextEncoderPolyfill.prototype.encode=function(e){for(var t,o=[],n=0;n<e.length;n++)(t=e.charCodeAt(n))<128?o.push(t):t<2048?o.push(192|t>>6,128|63&t):55296==(64512&t)&&n+1<e.length&&56320==(64512&e.charCodeAt(n+1))?(t=65536+((1023&t)<<10)+(1023&e.charCodeAt(++n)),o.push(240|t>>18,128|t>>12&63,128|t>>6&63,128|63&t)):o.push(224|t>>12,128|t>>6&63,128|63&t);return new Uint8Array(o)},window.TextEncoder||(window.TextEncoder=TextEncoderPolyfill),cl.forEach=function(e,t){e&&"object"==typeof e&&Object.keys(e).forEach((function(o){t(e[o],o)}))};var startTime=0;cl.upTime=function(){return startTime&&Math.min(Date.now()-startTime,1)};var toHex=cl.toHex=function(e){for(var t="",o=0;o<e.length;o++)t+=e[o]<16?"0"+e[o].toString(16):e[o].toString(16);return t},watchdog=cl.watchdog=function(e,t,o,n){var r=setTimeout((function(){r=0,t(new Error(n||"watchdog-timeout"))}),o||1e3);try{e((function(e){r&&(clearTimeout(r),t(e))}))}catch(e){clearTimeout(r),t(e)}},getDigest=cl.getDigest=function(e,t,o){try{"function"==typeof t&&(o=t,t="sha-256");var n=window.crypto||window.msCrypto,r=n&&(n.subtle||n.webkitSubtle);if(!r)return void o(0);var c=r.digest(t,(new TextEncoder).encode(e));watchdog((function(e){c.then?c.then(e):c.oncomplete=function(t){e(t.target.result)}}),o)}catch(e){o(e)}},startXhr=function(e,t,o,n){try{var r=new window.XMLHttpRequest;return r.open(e,t),r.timeout=1e5,r.withCredentials=!0,r.addEventListener("load",(function(){try{if(r.status>=200&&r.status<400)o(JSON.parse(r.responseText));else{var e=new Error("bad-xhr-status ("+r.status+")");e.xhr=r,n(e)}}catch(e){n(e)}})),["error","timeout","abort"].forEach((function(e){r.addEventListener(e,(function(e){n(e)}))})),r}catch(e){n(e)}return 0},LOGGED_KEY="logged_v1",localStorageIsAvailable=!1,logged=function(){try{var e=localStorage.getItem(LOGGED_KEY);try{(e=e?JSON.parse(e):{})&&"object"==typeof e||(e={})}catch(t){e={}}return localStorage.setItem(LOGGED_KEY,JSON.stringify(e)),localStorageIsAvailable=!0,e}catch(e){}return{}}(),setLogged=function(e){try{if(logged[e]=Date.now(),!localStorageIsAvailable)return;localStorage.setItem(LOGGED_KEY,JSON.stringify(logged));var t=cl.localStorage;t&&t.isPersistent&&t.setJsonItem(t.keys.logged,logged)}catch(e){console.error(e)}},synchronizeLogged=function(e){try{var t=e.getJsonItem(e.keys.logged)||{};t&&"object"==typeof t||(t={}),cl.forEach(t,(function(e,t){logged[t]=logged[t]||e}));var o={};Object.keys(logged).map((function(e){return[e,logged[e]]})).sort((function(e,t){return t[1]-e[1]})).slice(0,100).forEach((function(e){o[e[0]]=e[1]})),logged=o,e.setJsonItem(e.keys.logged,o),localStorage.setItem(LOGGED_KEY,JSON.stringify(o))}catch(t){try{e.setJsonItem(e.keys.logged,{}),localStorage.setItem(LOGGED_KEY,"{}")}catch(e){}cl.unexpected(bootError("synchronizeLogged-exception",t))}},DISPOSITION_PREVIOUSLY_LOGGED=1,DISPOSITION_LOGGED=2,DISPOSITION_CACHED=3,DISPOSITION_FAILED=4,DISPOSITION_DRAINED=5,reportedLogFailure=0;cl.log=function(e,t,o){var n=function(t,n){n&&setLogged(e.id),e.disposition=t;try{o&&o(e)}catch(e){cl.unexpected(e)}};try{if(!e.id){var r=JSON.stringify(e);return void getDigest(r,(function(n){try{e.id="?",e.id=r.length.toString(16),n instanceof ArrayBuffer&&(e.id=toHex(new Uint8Array(n)))}catch(t){e.id||(e.id="exception-log-id-log")}cl.log(e,t,o)}))}var c=JSON.stringify(e);if(t&&logged[e.id])return void n(DISPOSITION_PREVIOUSLY_LOGGED,!1);var a=window.location.origin+"/jslog",s=e.tid=(Math.random()+"").substring(2),i="cl-jslog-tid",l=function(){var e=startXhr("post",a,(function(e){n(1===e?DISPOSITION_LOGGED:DISPOSITION_FAILED,1===e)}),(function(){n(DISPOSITION_FAILED,!1)}));e&&(e.setRequestHeader("Content-type","application/json; charset=utf-8"),e.setRequestHeader(i,s),e.send(c))},u=startXhr("get",a+"?id="+e.id,(function(e){e===s?l():n(DISPOSITION_CACHED,!0)}),l);u&&(u.setRequestHeader(i,s),u.send())}catch(e){reportedLogFailure||(reportedLogFailure=1,cl.unexpected(bootError("log-exception",e))),n(DISPOSITION_FAILED,!1)}};var unexpectedQ=[],drainUnexpectedQFailure=0,drainUnexpectedQ=function(){if(!unexpectedQ.draining){unexpectedQ.draining=!0;var e=0,t=function(e){try{e.callback&&e.callback(e)}catch(e){}},o=function(o){t(o),e++,0===unexpectedQ.length?unexpectedQ=[]:e>=3?(unexpectedQ.slice().forEach((function(e){e.disposition=DISPOSITION_DRAINED,t(e)})),unexpectedQ=[]):n()},n=function(){var e=unexpectedQ.shift();try{if(e.id)return void cl.log(e,!0,o);var t=JSON.stringify(e);t=t.replace(/\w+\.craigslist\.org/g,"x.craigslist.org").replace(/x\.craigslist\.org\/static\/d\/\d+\/www\/manifest\.js/g,"manifest.js"),getDigest(t,(function(n){try{e.id="?",e.id=t.length.toString(16),n instanceof ArrayBuffer&&(e.id=toHex(new Uint8Array(n)))}catch(e){}if(logged[e.id])return e.disposition=DISPOSITION_PREVIOUSLY_LOGGED,void o(e);e.href=function(){try{return window.location.href}catch(e){return"error"}}(),cl.collectBfpForLogId[e.id]&&cl.getBfp3?watchdog((function(e){cl.getBfp3((function(t){t&&"object"==typeof t&&(delete t.pow,delete t.fonts,delete t.canvas),e(t)}))}),(function(t){t instanceof Error?e.bfp={error:1}:e.bfp=t,cl.log(e,!0,o)}),3e3):cl.log(e,!0,o)}))}catch(t){drainUnexpectedQFailure||(drainUnexpectedQFailure=1,cl.unexpected(bootError("drainUnexpectedQ-exception",t))),e.disposition=t,o()}};n()}},getErrorLogObject=function(e){var t={uptime:cl.upTime(),error:function(){try{return e+""}catch(e){return"failed to stringify error"}}()};return e&&e.callback&&(t.callback=e.callback),t.stack=function(e){try{if(!e)try{throw new Error("tracing")}catch(t){e=t.stack}return(e+"").split("\n").slice(0,10)}catch(e){return"error"}}(e&&e.stack),t.scripts=function(){try{for(var e=document.getElementsByTagName("script"),t=[],o=0;o<e.length;o++)e[o].src&&t.push(e[o].src);return t}catch(e){return"error"}}(),t};cl.unexpected=function(e){try{if(console.error(e),e||(e=bootError("unexpected",new Error("no error provided"))),e.useless||/SyntaxError/.test(e+"")&&0===cl.injectingJsCount||!/www.craigslist.org/.test(e.stack+"")&&!(e instanceof CLError))return e;var t=e.id?e:getErrorLogObject(e);return unexpectedQ.push(t),drainUnexpectedQ(),t}catch(e){return e}};var docLoading=!0,errorDuringDocLoad=0;window.addEventListener("error",(function(e){if(docLoading)errorDuringDocLoad=e||"unknown error";else{var t=globalErrorToError(e,"globalError");e.filename&&"pending"===cl.onLoadingResourcesComplete.status[e.filename]&&(t=cl.onLoadingResourcesComplete.status[e.filename]=bootError("loading-resource",t)),cl.unexpected(t)}}));try{cl.oldBrowser=cl.devKnobs&&cl.devKnobs.oldBrowser||!(doc.currentScript&&"noModule"in doc.currentScript),eval("(function(){let x = {};let y = {...x};})();")}catch(e){cl.oldBrowser=!0}var curtainStack=[];cl.pushCurtain=function(e,t){var o=["show-curtain"];e&&(o=o.concat(e.trim().split(/\s+/))),t&&o.push("message");var n={classNames:o,message:t||0};return clearCurtain(curtainStack.length&&curtainStack[curtainStack.length-1]),curtainStack.push(n),setCurtain(n),n},cl.popCurtain=function(e){if(void 0===e){if(!curtainStack.length)return;e=curtainStack[curtainStack.length-1]}var t=curtainStack.indexOf(e);-1===t?clError("handle not found","curtain",!0):t===curtainStack.length-1?(clearCurtain(e),curtainStack.pop(),setCurtain(curtainStack.length&&curtainStack[curtainStack.length-1])):curtainStack.splice(t,1)};var cookies=cl.bootCookies=function(){var e={};try{doc.cookie.split(";").forEach((function(t){var o=(t||"").split("=").map((function(e,t){e=e.trim(),t&&/^".+"$/.test(e)&&(e=e.substring(1,e.length-1).trim());try{return decodeURIComponent(e)}catch(e){return cl.unexpected(bootError("bootCookies-exception",e)),""}}));o[0]&&(e[o[0]]=o[1])}))}catch(e){}return e}();cl.runProcQueue=function(e,t,o,n){if(Array.isArray(e)){for(var r=e.length+(o||0)+1;e.length&&--r;)try{e.shift()(t)}catch(e){cl.unexpected(e)}r||cl.unexpected(new Error(n||"svs-watchdog-barked"))}},cl.createCallbackQueue=function(e,t){var o,n=[],r=!1,c=function(a){if(a&&n.push(a),o&&!r){r=!0;for(var s=n.length+(e||0)+1,i=t?!c.isLocked()&&o:o;i&&n.length&&s>1;)s-=n.length,n.splice(0,n.length).forEach((function(e){try{e()}catch(e){c.errors.push(e),cl.unexpected(e)}})),i=t?!c.isLocked()&&o:o;if(s<1){var l=new Error("svs-watchdog-barked");c.errors.push(l),cl.unexpected(l)}r=!1}};if(c.q=n,c.errors=[],c.signal=function(e){o=e,c()},t){var a=c.locks={};c.lockExists=function(e){return e in a},c.isLocked=function(){return Object.keys(a).some((function(e){return a[e]}))},c.lock=function(e){a[e]=!0,c.signal(null)},c.unlock=function(e){a[e]=!1,c.isLocked()||c.signal(Object.keys(a))}}return c},cl.onDomReady=cl.createCallbackQueue(10),cl.onLoad=cl.createCallbackQueue(10),window.addEventListener("load",(function(e){cl.onLoad.signal(e)})),cl.onLoadingResourcesComplete=cl.createCallbackQueue(0,!0),cl.onLoadingResourcesComplete.status={},cl.onStagingComplete=cl.createCallbackQueue(10,!0),cl.onCssComplete=cl.createCallbackQueue(10,!0);var insertPoint=getInsertPoint();cl.injectCss=function(e,t){if(!cl.onCssComplete.lockExists(e)){var o=doc.createElement("link");o.type="text/css",o.rel="stylesheet",o.href=e,o.onload=function(){t&&t(),cl.onCssComplete.unlock(e)},cl.onCssComplete.lock(e),insertPoint.parentNode.insertBefore(o,insertPoint)}},cl.injectingJsCount=0,cl.injectJs=function(e,t,o,n){if(!cl.onLoadingResourcesComplete.status[e]){cl.onLoadingResourcesComplete.status[e]="pending",cl.onLoadingResourcesComplete.lock(e);var r=doc.createElement("script");r.type=o?"module":"text/javascript",r.src=e,n&&(r.crossOrigin="string"==typeof n?n:"use-credentials");var c=0;t&&(c=function(e){try{t(e)}catch(e){cl.unexpected(e)}}),r.addEventListener("load",(function(){if(cl.injectingJsCount--,cl.onLoadingResourcesComplete.status[e]instanceof Error)return c&&c(cl.onLoadingResourcesComplete.status[e]),void cl.onLoadingResourcesComplete.unlock(e);c&&c(),cl.onLoadingResourcesComplete.status[e]="loaded",cl.onLoadingResourcesComplete.unlock(e)})),r.addEventListener("error",(function(t){if(cl.injectingJsCount--,!(cl.onLoadingResourcesComplete.status[e]instanceof Error)){var o=bootError("injectJs-error",globalErrorToError(t,"loadError"),e);cl.unexpected(o),cl.onLoadingResourcesComplete.status[e]=o}c&&c(cl.onLoadingResourcesComplete.status[e]),cl.onLoadingResourcesComplete.unlock(e)})),cl.injectingJsCount++,insertPoint.parentNode.insertBefore(r,insertPoint)}},cl.injectEsm=function(e,t,o){cl.injectJs(e,t,!0,o)},cl.manifest={},cl.resources=[],cl.amdFactories={};var AMD_FACTORY_DEPS=0,AMD_FACTORY_FACTORY=1,AMD_FACTORY_ORDER=2;cl.amdModules={},cl.Rir=function(e,t){var o=e[0].match(/^([^.]+)\.(.+)$/);this.name=e[0],this.sha1=e[2],this.amdId=/js$/.test(o[2])&&o[1],this.type=o[2],this.es5="es5.js"===o[2],this.vFilename=o[1]+"-"+e[1]+"-"+e[2]+"."+this.type,this.immediate=e[3],this.src=e[4],this.url=(cl.devRoot||cl.staticRoot)+(this.src||this.vFilename),this.order=t,this.staged=null},cl.injectResource=function(e,t){if(null===e.staged)if(/js$/.test(e.type)){var o=cl.devRoot?function(e){t&&t(e)}:function(o){"function"==typeof e.staged||(e.staged=o||bootError("injectResource",new Error("no-staging-function")),t&&t(o))};e.es5||cl.oldBrowser?e.es5&&cl.oldBrowser&&(cl.devRoot&&e.src&&Array.isArray(e.src)?e.src.forEach((function(e){cl.injectJs(cl.devRoot+e,o)})):(e.staged=!1,cl.injectJs(e.url,o,!1,"anonymous"))):cl.devRoot?cl.injectEsm(e.url,o):(e.staged=!1,cl.injectJs(e.url,o,!1,"anonymous"))}else cl.injectCss(e.url,t)},cl.resourceByName=function(e){var t;return cl.resources.some((function(o){return o.name===e&&(t=o)})),t},cl.resourceByAmdId=function(e){var t;return cl.resources.some((function(o){return o.amdId===e&&(o.es5||cl.oldBrowser?o.es5&&cl.oldBrowser&&(t=o):t=o),t})),t},cl.resourceByUrl=function(e){var t;return cl.resources.some((function(o){return o.url===e&&(t=o)})),t},cl.prestagedResources={},cl.stage=function(e,t){var o=e&&cl.resourceByName(e);o?!0!==o.staged&&(o.staged=t,cl.onStagingComplete.lock(o.sha1),cl.stage.hold||(cl.runningStagingFactory?runStagingFactory(o):runStagingFactories())):cl.prestagedResources[e]=t},cl.lazyLoad=function(e,t){/\.js$/.test(e)&&cl.oldBrowser&&(e=e.replace(/\.js$/,".es5.js"));var o=cl.resourceByName(e);return o&&cl.injectResource(o,t),o},window.define=function(e,t,o){function n(){var e=Object.keys(cl.amdFactories),t=e.length;return e.forEach((function(e){cl.amdFactories[e][AMD_FACTORY_DEPS].forEach((function(e){t=t&&("exports"===e||cl.amdModules[e]||cl.amdFactories[e])}))})),t}function r(e){if(cl.amdModules[e])return cl.amdModules[e];var t=cl.amdFactories[e][AMD_FACTORY_DEPS],o=cl.amdFactories[e][AMD_FACTORY_FACTORY];delete cl.amdFactories[e];var n=cl.amdModules[e]={},c=t.map((function(e){return"exports"===e?n:r(e)}));try{return cl.amdModules[e]=o.apply(window,c)||n}catch(t){return cl.runningStagingFactory?cl.runningStagingFactory=bootError("amd-exec-exception",t):cl.unexpected(t),cl.amdModules[e]=t}}var c,a;for(o||(o=t,t=[]),t=t.map((function(e){return"exports"!==e&&cl.injectResource(cl.resourceByAmdId(e=e.substring(2))),e})),cl.amdFactories[e]=[t,o,cl.resourceByAmdId(e).order];n();)c=0,a=1e4,cl.forEach(cl.amdFactories,(function(e,t){!cl.amdModules[t]&&e[AMD_FACTORY_ORDER]<a&&(c=t,a=e[AMD_FACTORY_ORDER])})),c&&r(c)};var windowMessageCache=[],windowMessageHandlers=[],recordWindowMessages=!0;window.addEventListener("message",(function(e){windowMessageHandlers.slice().forEach((function(t){try{t(e)}catch(e){cl.unexpected(e)}})),recordWindowMessages&&windowMessageCache.push(e)})),cl.adviseWindowMessage=function(e){windowMessageCache.forEach((function(t){try{e(t)}catch(e){cl.unexpected(e)}})),windowMessageHandlers.push(e)},cl.unadviseWindowMessage=function(e){for(var t=0,o=windowMessageHandlers.length;t<o;t++)if(windowMessageHandlers[t]===e){windowMessageHandlers.splice(t,1);break}};var bigBang=function(){cl.resources=cl.manifest[cl.resourceSetName]||[],cl.onStagingComplete((function(){cl.bootCurtain&&cl.popCurtain(cl.bootCurtain),cl.localStorage&&cl.localStorage.then(synchronizeLogged),recordWindowMessages=!1,startTime=Date.now(),/\.craigslist\.org$/.test(window.location.host)||cl.beacon("svs-foreign host:"+window.location.host);try{window.location===window.parent.location||/\.craigslist\.org$/.test(window.parent.hostname)||cl.beacon("svs-iframed:"+window.parent.location)}catch(e){}}));var e=[];cl.resources.forEach((function(t){t.immediate&&e.push(t)})),injectResourceSet(e,(function(t){if("ok"!==t)if(cl.oldBrowser)cl.showUnrecoverableMessage();else{errorDuringDocLoad=0,cl.prestagedResources={};var o=0;e.forEach((function(e){e.staged instanceof Error&&(o=o||e.staged,e.staged=null),"function"==typeof e.staged&&(e.staged=null)})),cl.onLoadingResourcesComplete.status={},Object.keys(cl.onStagingComplete.locks).forEach((function(e){delete cl.onStagingComplete.locks[e]})),cl.amdModules={},cl.oldBrowser="retrograde",injectResourceSet(e,(function(e){"ok"===e?(cl.initialStageComplete=!0,cl.unexpected(bootError("retrograde",o||new Error("no bad resource found")))):cl.showUnrecoverableMessage()}))}else cl.initialStageComplete=!0}))};cl.setManifest=function(e){try{if(ignoreFirstManifest)return;cl.setManifest=0,cl.rawManifest=e,Object.keys(e).forEach((function(t){var o=e[t];Array.isArray(o)?cl.manifest[t]=o.map((function(e,t){return new cl.Rir(e,t)})):cl[t]=o})),cl.onDomReady(bigBang)}catch(e){cl.unexpected(bootError("setManifest-exception",e)),cl.showUnrecoverableMessage()}};var manifestCookie=cookies.cl_manifest,ignoreFirstManifest=!!manifestCookie,manifestUrl=cl.staticRoot+(manifestCookie||"manifest.js");if(/www\.craigslist\.org/.test(manifestUrl)){var cacheBust=Math.floor(Date.now()/3e5);manifestUrl=manifestUrl.replace(/\/static\//,"/static/d/"+cacheBust+"/")}else manifestUrl+=(/\?/.test(manifestUrl)?"&":"?")+"cacheBust="+Date.now();doc.addEventListener("DOMContentLoaded",(function(e){try{if(docLoading=!1,cl.unsupportedBrowser)return;cl.beacon("start");var t=doc.body.classList;if(t.contains("show-curtain")){var o=[];"loading.reading.writing.saving.searching.text.opaque.pacify".split(".").forEach((function(e){t.contains(e)&&o.push(e)})),cl.bootCurtain=cl.pushCurtain(o.join(" "),document.querySelector("#curtain .text.message").innerHTML)}injectManifest(),cl.onDomReady.signal(e)}catch(e){cl.unexpected(bootError("DOMContentLoaded-exception",e))}}))}function removeNode(e){try{e&&e.parentNode&&e.parentNode.removeChild(e)}catch(e){}}function bootError(e,t,o){return t instanceof Error||(t=new Error(t.message||"bootError-bad-error-object")),o=o?" ("+o+")":"",t.message="svs-boot-"+e+":"+t.message+o,t.additionalInfo=o,t}function CLError(e,t){this.msg=e+"",this.stack=t||""}function clError(e,t,o){var n=new CLError(e,t);return o&&cl.unexpected(n),n}function clearCurtain(e){e&&(e.classNames.forEach((function(e){document.body.classList.remove(e)})),doc.querySelector("#curtain .text.message").innerHTML="")}function setCurtain(e){e&&(e.classNames.forEach((function(e){e&&document.body.classList.add(e)})),e.message&&(document.querySelector("#curtain .text.message").innerHTML=e.message))}function getInsertPoint(){try{return doc.getElementsByTagName("script")[0]}catch(e){}return 0}function createStagingError(e,t){if(e instanceof Error)return e.message="staging-exception("+t.vFilename+"):\n"+e.message,e;var o=new Error("staging-exception-synthetic("+t.vFilename+"):\n"+e);return o.stack=e.stack||o.stack,o}function runStagingFactory(e){var t=cl.runningStagingFactory;try{if(cl.runningStagingFactory=!0,e.staged(),cl.runningStagingFactory instanceof Error)throw cl.runningStagingFactory;e.staged=!0,cl.onStagingComplete.unlock(e.sha1)}catch(t){cl.unexpected(cl.stage.hold=e.staged=createStagingError(t,e))}cl.runningStagingFactory=t}function runStagingFactories(){for(var e=0;e<cl.resources.length&&!cl.stage.hold;e++){var t=cl.resources[e];if(!1===t.staged)return;"function"==typeof t.staged&&runStagingFactory(t)}}function injectResourceSet(e,t){cl.stage.hold=!0,cl.onStagingComplete.lock("injecting-set"),cl.onLoadingResourcesComplete.lock("injecting-set"),cl.onCssComplete.lock("injecting-set"),e.forEach((function(e){document.getElementById(e.sha1)?cl.prestagedResources[e.name]&&cl.stage(e.name,cl.prestagedResources[e.name]):cl.injectResource(e)})),cl.onCssComplete.unlock("injecting-set"),cl.onLoadingResourcesComplete.unlock("injecting-set"),cl.onLoadingResourcesComplete((function(){try{if(!errorDuringDocLoad&&e.every((function(e){return null===e.staged||"function"==typeof e.staged})))return void cl.onCssComplete((function(){cl.onStagingComplete.unlock("injecting-set"),cl.stage.hold=!1,runStagingFactories(),!1===cl.stage.hold?t("ok"):(cl.stage.hold=cl.stage.hold||!0,cl.onStagingComplete.lock("injecting-set"),t("error"))}))}catch(e){cl.unexpected(bootError("onLoadingResourcesComplete-exception",e))}cl.stage.hold=cl.stage.hold||!0,cl.onStagingComplete.lock("injecting-set"),t("error")}))}function injectManifest(){document.getElementById("manifest")&&!ignoreFirstManifest||(ignoreFirstManifest=!1,(insertPoint=getInsertPoint())&&insertPoint.parentNode?cl.injectJs(manifestUrl,(function(e){e&&cl.showUnrecoverableMessage()}),!1,"anonymous"):cl.showUnsupportedMessage("failed_insert_point"))}},cl.init=function(e,t,o,n,r,c){try{cl.init_(e,t,o,n,r,c),cl.unsupportedBrowser||(window.onload=null)}catch(e){cl.unsupportedBrowser="init-error:"+e+(e&&e.stack?"("+e.stack+")":0)}};