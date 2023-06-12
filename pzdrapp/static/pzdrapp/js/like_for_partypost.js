<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.js"></script>
<script type="text/javascript">
  const likePartypostButtons = document.getElementsByClassName('ajax-like-for-partypost');
  console.log(likePartypostButtons)
  for (const button of likePartypostButtons) {
    button.addEventListener('click', e => {
      const pk = button.dataset.pk
      e.preventDefault();
      const url = '{% url "like_for_partypost" %}';
      fetch(url, {
        method: 'POST',
        body: `partypost_pk=${pk}`,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
          'X-CSRFToken': '{{ csrf_token }}',
        },
      }).then(response => {
        return response.json();
      }).then(response => {
        const counter = document.getElementById(`like-for-partypost-count-${pk}`)
        const icon = document.getElementById(`like-for-partypost-icon-${pk}`)
        counter.textContent = response.like_for_partypost_count
        if (response.method == 'create') {
          icon.classList.remove('far')
          icon.classList.add('fas')
          icon.id = `like-for-partypost-icon-${pk}`
        } else {
          icon.classList.remove('fas')
          icon.classList.add('far')
          icon.id = `like-for-partypost-icon-${pk}`
        }
      }).catch(error => {
        console.log(error);
      });
    });
  }
</script>