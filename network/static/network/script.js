document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.edit-buttons').forEach(editBtn => {
        editBtn.onclick = () => {
            // Get id & content of the current Post object
            const postId = editBtn.getAttribute('data-post-id')
            const contentElement = document.querySelector(`#content-${postId}`)
            const postContent = contentElement.innerText

            // Create textarea and save button & replace editBtn w saveBtn; div w prepopulated textarea
            const textarea = document.createElement('textarea')
            textarea.value = postContent
            const saveBtn = document.createElement('button')
            saveBtn.className = 'buttons'
            saveBtn.innerText = 'Save'
            editBtn.replaceWith(saveBtn)
            contentElement.replaceWith(textarea)

            // 'Click' listener for the saveBtn: save the new content, retrieve back what was before
            saveBtn.onclick = () =>
                fetch(`/edit/${postId}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        content: textarea.value
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if(data.success) {
                        const newContent = document.createElement('div')
                        newContent.id = `content-${postId}`
                        newContent.style.fontSize = '1.3em'
                        newContent.innerText = textarea.value
                        textarea.replaceWith(newContent)
                        saveBtn.replaceWith(editBtn)
                    }
                    else {
                        console.log("Error with editing the content of the post.")
                    }
                })
        }
    })

    // 'Click' listener for the like buttons: PUT request to '/like/' API, from the response, either increment or decrement
    document.querySelectorAll('.like-buttons').forEach(likeBtn => {
        likeBtn.onclick = () => {
            const postId = likeBtn.getAttribute('data-post-id')
            fetch(`/like/${postId}`, {
                method: "PUT",
                body: JSON.stringify({
                    likes: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {

                    // Get the current posts like counter by the id defined in index.html & change the num of likes corresponding to the response
                    const likesCountElement = document.querySelector(`#likes-count-${postId}`)
                    let likesCount = parseInt(likesCountElement.innerText)
                    if(data.like) {
                        likesCountElement.innerText = `${likesCount+1}`
                        likeBtn.className = "invisible-buttons"
                        likeBtn.innerHTML = `<i class="fa-solid fa-heart" style="color: #ff0000;"></i>`
                    }
                    else {
                        likesCountElement.innerText = `${likesCount-1}`
                        likeBtn.className = "invisible-buttons"
                        likeBtn.innerHTML = `<i class="fa-regular fa-heart">`
                    }
                }
            })
        }
    })
})
