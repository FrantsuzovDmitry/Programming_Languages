package main

import (
	"fmt"
	"time"
)

type Token struct {
	Data      string
	Recipient int
	TTL       int // Time to live (0, ...]
}

func node(id int, in <-chan Token, out chan<- Token) {
	// while (true)
	for {
		token := <-in
		fmt.Printf("Node %d received token: %+v\n", id, token)

		if token.Recipient == id {
			fmt.Printf("Node %d received the message: %s\n", id, token.Data)
			continue
		}

		if token.TTL > 0 {
			token.TTL--
			out <- token
		} else {
			fmt.Printf("Node %d: TTL expired for token: %s\n", id, token.Data)
		}
	}
}

func main() {
	var N int
	fmt.Println("Enter the number of nodes:")
	fmt.Scanln(&N)

	// Initialization
	channels := make([]chan Token, N)
	for i := range channels {
		channels[i] = make(chan Token)
	}

	// Goroutines start
	for i := 0; i < N-1; i++ {
		go node(i, channels[i], channels[i+1])
	}
	go node(N-1, channels[N-1], channels[1])

	//-----Inputs-------//
	fmt.Println("Enter message data:")
	var message string
	fmt.Scanln(&message)

	fmt.Println("Enter recipient node (0 to", N-1, "):")
	var recipient int
	fmt.Scanln(&recipient)
	if recipient < 0 || recipient > N-1 {
		fmt.Println("Invalid recipient node")
		return
	}

	fmt.Println("Enter TTL:")
	var ttl int
	fmt.Scanln(&ttl)
	//-----------------//

	initialToken := Token{Data: message, Recipient: recipient, TTL: ttl}
	channels[0] <- initialToken

	// Close program in 3s
	time.Sleep(time.Second * 3)
}
