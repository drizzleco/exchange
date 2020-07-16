import axios from 'axios'
import store from './store'
import router from './router'

const apiUrl = "http://localhost:5000/"

/**
 * Redirects to home route if user is already logged in
 */
export function redirectIfLoggedIn() {
    if (store.getters.loggedIn) router.push("/");
}

/**
 * Generic axios POST request
 * @param {string} path path to send request to
 * @param {Object} data data to send 
 * @returns {Promise}   axios Promise
 */
export function post(path, data) {
    return axios
        .post(apiUrl + path, data, {
            withCredentials: true
        })
}

/**
 * Generic GraphQL query
 * @param {string} query GraphQL query to send
 * @param {Object} vars GraphQL variables, if necessary
 * @returns {Promise}   axios Promise
 */
function graphql(query, vars = {}) {
    return post("graphql", {
        query: query,
        variables: vars
    })
}

/**
 * GraphQL query to get all auctions
 * @returns {Promise}   axios Promise
 */
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

/**
 * GraphQL query to get info for an Auction
 * @param {string|number} id id of Auction to retrieve
 * @returns {Promise} axios Promise
 */
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

/**
 * GraphQL mutation to create Bid for an Auction
 * @param {string|number} auction_id id of Auction to create Bid for
 * @param {number} amount amount of Bid
 * @returns {Promise}     axios Promise
 */
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

/**
 * GraphQL mutation to create a new Auction
 * @param {string} name name of Auction
 * @param {string} description description of Auction
 * @param {float} startingPrice starting price of Auction
 * @param {string} endTime end time of Auction in format "yyyy-mm-dd hh:mm"
 * @returns {Promise}   axios Promise
 */
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

/**
 * GraphQL query to get info for a user
 * @param {string} username username of user to get
 * @returns {Promise}  axios Promise
 */
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

/**
 * Set a cookie(with an expiration) to a value
 * @param {string} name name of cookie
 * @param {string} value value to set
 * @param {number} days number of days till cookie's expiration
 */
export function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

/**
 * Get value of cookie from browser
 * @param {string} name name of cookie to retrieve
 * @returns {string}    value of cookie
 */
export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

/**
 * Check if cookie exists
 * @param {string} name name of cookie to check for
 * @returns {boolean}    true if cookie exists
 */
export function cookieExists(name) {
    return document.cookie.indexOf(name + '=') >= 0;
}

/**
 * Delete a cookie from browser
 * @param {string} name name of cookie to delete
 */
export function eraseCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

/**
 * Format a number of seconds to a nice string with days, hour, minute, and seconds
 * @param {number} seconds seconds to format
 * @returns {string}    formatted string(ex: 15 days, 22 hours, 35 minutes, 49 seconds)
 */
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

/**
 * Convert a UTC date string to the user's respective locale
 * @param {string} date_string date string to format
 * @returns {string}    formatted locale string
 */
export function formatDate(date_string) {
    return new Date(date_string.split('.')[0] + 'Z').toLocaleString()
}

/**
 * Covert a number to USD currency string
 * @param {number} number number to format
 * @returns {string}    USD formatted string
 */
export function formatMoney(number) {
    var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    });

    return formatter.format(number);
}
