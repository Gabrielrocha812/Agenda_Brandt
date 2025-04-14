document.addEventListener("DOMContentLoaded", function() {
    // Carregar os usuários e grupos quando a página carregar
    fetch('/api/get-users')  // Endpoint que retorna a lista de usuários
        .then(response => response.json())
        .then(data => {
            if (data.users) {
                const userTableBody = document.getElementById("user-table-body");
                data.users.forEach(user => {
                    const row = document.createElement("tr");

                    // Cria as células da tabela
                    const usernameCell = document.createElement("td");
                    usernameCell.textContent = user.username;

                    const fullNameCell = document.createElement("td");
                    fullNameCell.textContent = user.full_name;

                    const groupCell = document.createElement("td");
                    groupCell.textContent = user.group_name;

                    const actionsCell = document.createElement("td");

                    // Cria o campo de seleção de grupo
                    const selectGroup = document.createElement("select");
                    user.groups.forEach(group => {
                        const option = document.createElement("option");
                        option.value = group.name;
                        option.textContent = group.name;
                        selectGroup.appendChild(option);
                    });

                    selectGroup.addEventListener("change", function() {
                        const selectedGroup = selectGroup.value;
                        updateUserGroup(user.username, selectedGroup);
                    });

                    actionsCell.appendChild(selectGroup);

                    // Adiciona as células à linha
                    row.appendChild(usernameCell);
                    row.appendChild(fullNameCell);
                    row.appendChild(groupCell);
                    row.appendChild(actionsCell);

                    // Adiciona a linha à tabela
                    userTableBody.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('Error loading users:', error);
        });

    // Função para atualizar o grupo do usuário
    function updateUserGroup(username, newGroup) {
        fetch('/api/assign-group', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username, group_name: newGroup })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || 'Erro ao atualizar o grupo.');
            // Recarregar a tabela de usuários
            location.reload();
        })
        .catch(error => {
            console.error('Error updating user group:', error);
            alert('Erro ao atualizar o grupo.');
        });
    }
});
