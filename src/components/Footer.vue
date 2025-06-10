<script setup>
</script>

<template>
    <footer>
        <div>
            <RouterLink to="/">Collection</RouterLink>
            <RouterLink to="/upload">Upload Artifact</RouterLink>
            <RouterLink to="/">Terms and conditions</RouterLink>
            <RouterLink to="/">Copyright</RouterLink>
        </div>
    </footer>
</template>

<style scoped>
footer {
    display: flex;
    gap: 40px;
    width: 100vw;
    background-color: black;
}

div {
    display: flex;
    flex-direction: row;
    justify-content: left;
    gap: 40px;
    max-width: 1280px;
    width: 100%;
    margin: 0 auto;
    padding: 2rem;
    font-weight: normal;
}

a {
  color: rgb(180, 180, 180);         /* or any color you prefer */
  text-decoration: underline; /* optional: remove underline */
}

a:hover {
    text-decoration: none;
}
</style>