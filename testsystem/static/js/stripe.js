async function pressBuyButton(id) {
    try{
        const response = await fetch(`/buy/${id}`, { method: 'GET' });
        const data = await response.json();
        
        if (data.error) {
            console.error('Error:', data.error);
            return;
        }
        
        window.location.href = data.session_url
    }catch(error){
        console.error('Error:', error);
    }

}
