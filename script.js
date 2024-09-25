const botao = document.querySelector('#botao');
const eventoBotao = () => {
    botao.addEventListener('click',() =>{
       window.location.replace('file:///D:/fecart/index.html');
    })
}
window.onload = () => {
 eventoBotao();

}
