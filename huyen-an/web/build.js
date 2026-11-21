// Đóng gói web/game.html thành trang đầy đủ cho WebView Android (font nằm trong máy, không cần mạng).
const fs=require('fs'),path=require('path');
const out=path.join(__dirname,'../android/app/src/main/assets');
fs.mkdirSync(path.join(out,'fonts'),{recursive:true});
let body=fs.readFileSync(path.join(__dirname,'game.html'),'utf8').replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>\n?/,'');
const fonts=fs.readFileSync(path.join(__dirname,'fonts.css'),'utf8');
const head=`<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<style>${fonts}
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box;height:100%}
body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>`;
fs.writeFileSync(path.join(out,'index.html'),head+body+'</body></html>');
for(const f of fs.readdirSync(path.join(__dirname,'fonts')))fs.copyFileSync(path.join(__dirname,'fonts',f),path.join(out,'fonts',f));
if(fs.existsSync(path.join(__dirname,'art'))){fs.mkdirSync(path.join(out,'art'),{recursive:true});fs.cpSync(path.join(__dirname,'art'),path.join(out,'art'),{recursive:true})}
console.log('assets →',out);
