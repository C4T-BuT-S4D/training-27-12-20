package main

import (
    "encoding/binary"
    "encoding/hex"
    "fmt"
    "os"

    "github.com/dchest/siphash"
)

func main() {
    f, err := os.Create("tokens.txt")
    if err != nil {
        panic(err)
    }
    defer f.Close()
    for i :=0; i < 10000; i++ {
        uid := fmt.Sprintf("%09d", i)
        x := siphash.Hash(0xdda7806a4847ec61, 0xb5940c2623a5aabd, []byte(uid))
        h := make([]byte, 8)
	    binary.LittleEndian.PutUint64(h, x)
	    hshs := hex.EncodeToString(h)
        cook := fmt.Sprintf("%s:%s", uid, hshs)
        fmt.Fprintln(f, cook)
    }
    
}
