-- here are some things that shouldnt work

class Foo inherits IO and IO {
    let fast in         -- the types are missing

    go_fast(Program)    
    {
        if not fast then
            -- if only it were this easy
            go_fast(Program)
        else
            true;
    }

    anotherfunct(): Lsdfsdfs {
        case x:False of     -- bools shouldnt be types
            y:True 
        in {
           x + y;
           xy;
           (x); 
           (new Something)@Object.function(new new Type) --expression list wrong
        }
    }
}

class Something {}


-- bits and pieces of nonsense code involving strings, booleans, classes, new, assignments, methods, init, inheritance, and more
Class Identifier inherits SomethingCool { -- try class inheritance and using a token term in the program itself
	main() {
             let l : Lister <- new Nil  -- missing a comma
                 done : Bool <- true    -- try out booleans
             {                          -- no "in"
               while not loop {    -- no condition
                 let s : String <- in_string () in 
                 if s <- "alpha" then       -- what would this even mean; broken if statement
                   done <- s         -- bool shouldnt get string
                 else 
                   done <- true 
                 fi;
               };                     -- loop/pool testing; no pool
               l.print_list ;            -- try methods no paren
             }
	};
};

Class Options inherits IO {         -- another class with inits
	statue(top : String) : Wishes { -- try garbage method
	  let new_wish : Wishes <- new Wishes in
		new_wish.init(top,self)    -- try initializing
	};

	printing_statue_plaque() : Object { abort() }; -- didn't want to bother writing a real action
} ;

Class Monarchy inherits Options {   -- more inherits with un-initialized attributes
	caption : String;         
	unused_attr : Options;           

	init(top : String, wishlist : List) : Monarchy { 
	  {
	    caption <- wishlist;      -- caption is String not List (let's disregard the face that List type isn't legitimate)
	    self;           -- can it handle self alone without context: identifiers
	  }
	};
} ;