import axios from 'axios'

export function post(path, data) {
    return axios
        .post("http://localhost:5000/" + path, data, {
            withCredentials: true
        })
}

function graphql(query, vars = {}) {
    return post("graphql", {
        query: query,
        variables: vars
    }, {
        withCredentials: true
    })
}

export function getAuctions() {
    return graphql(`
    {
        auctions {
            id
            name
            startingPrice
            description
            created
            endTime
            user {
                username
            }
            bids {
                id
                amount
                created
                user {
                    username
                }
            }
        }
    }
    `)
}

export function getAuction(id) {
    return graphql(`
        query auction($id: Int) {
            auctions(id: $id) {
                id
                name
                startingPrice
                description
                created
                endTime
                user {
                    username
                }
                bids {
                    id
                    amount
                    created
                    user {
                        username
                    }
                }
            }
        }
    `, {
        'id': id
    })
}

export function createBid(auction_id, amount) {
    return graphql(`
        mutation newBid($auctionId: Int!, $amount: Float!) {
            createBid(auctionId: $auctionId, amount: $amount) {
                bid {
                    id
                    amount
                    created
                    auction {
                        user {
                            username
                        }
                        startingPrice
                    }
                }
                message
            }
        }
    `, {
        auctionId: auction_id,
        amount: amount
    })
}

export function createAuction(name, description, startingPrice, endTime) {
    return graphql(`
    mutation newAuction($name: String!, $description: String!, $startingPrice: Float!, $endTime: String!) {
        createAuction(name: $name, description: $description, startingPrice: $startingPrice, endTime: $endTime) {
            auction {
                id
            }
            message
        }
    }
    `, {
        name: name,
        description: description,
        startingPrice: startingPrice,
        endTime: endTime
    })
}

export function getUser(username) {
    return graphql(`
    query user($username: String) {
        users(username: $username) {
            id
            username
            auctions {
                id
                name
                startingPrice
                description
                created
                endTime
                user {
                    username
                }
                bids {
                    id
                    amount
                    created
                    user {
                        username
                    }
                }
            }
            bids {
                id
                amount
                created
                auction {
                    id
                    name
                    user {
                        username
                    }
                }
                user {
                    username
                }
            }
        }
    }

    `, {
        username: username
    })
}

export function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

export function cookieExists(name) {
    return document.cookie.indexOf(name + '=');
}

export function eraseCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

export function formatSeconds(seconds) {
    let d = Math.floor(seconds / (3600 * 24));
    let h = Math.floor(seconds % (3600 * 24) / 3600);
    let m = Math.floor(seconds % 3600 / 60);
    let s = Math.floor(seconds % 60);

    let dDisplay = d + (d == 1 ? " day, " : " days, ");
    let hDisplay = h + (h == 1 ? " hour, " : " hours, ");
    let mDisplay = m + (m == 1 ? " minute, " : " minutes, ");
    let sDisplay = s + (s == 1 ? " second" : " seconds");
    return dDisplay + hDisplay + mDisplay + sDisplay;
}

export function formatDate(date_string) {
    return new Date(date_string.split('.')[0] + 'Z').toLocaleString()
}
