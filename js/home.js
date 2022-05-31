fetch("../web_docs/files.json")
.then(function(response){
    return response.json();
})
.then(function(files){
    let file1 = "";
    files.map(function(obj){
        file1 = `<article class="columns is-multiline">
        <div class="column is-12 post-img">
          <img src="${obj.image}" alt="Featured Image">
        </div>
        <div class="column is-12 featured-content">
          <h3 class="heading post-category">${obj.catagory}</h3>
          <h1 class="title post-title">${obj.title}</h1>
          <br>
          <a href="${obj.location}" class="button is-info">Open File</a>
        </div>
      </article>`
    })
    document.getElementById("posts").innerHTML = file1;

}).catch(function(err){
    console.error(err);
})
