-- these should work - even if they types dont

class Number1 inherits Something {
    a_function(): Object {
        let var: Int <- 12, variable: Bool <- true in {
            -- a block of text
            while variable loop
                print("a string!")
            pool;
            x;
        }
    };
};

-- add some more classes
ClasS Hey {
    hi(): String {
        "hello there"
    };
};

class Nothing {
    -- nothing in here
};

class Something {
    the_void(x: Object): Nothing {
        {
            isvoid x;
            "x is now nothing";
            while x + e loop
                x@Type.function()
            pool;
        }
    };
};


-- bits and pieces of nonsense code involving strings, booleans, classes, new, assignments, methods, init, inheritance, and more
Class Identifier inherits SomethingCool { -- try class inheritance and using a token term in the program itself
	main() : Object {
             let l : Lister <- new Nil, -- try out "new"
                 done : Bool <- true    -- try out booleans
             in {
               while not done loop {    -- try out while loop and not
                 let s : String <- in_string () in 
                 if s = "alpha" then        -- try out if statements
                   done <-true              -- try bindings
                 else 
                   done <- true 
                 fi;
               } pool ;                     -- loop/pool testing
               l.print_list () ;            -- try methods
             }
	};
};

Class Options inherits SomethingCooler {         -- another class with inits
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
	    caption <- new String;      -- using new
	    self;           -- can it handle self alone without context: identifiers
	  }
	};
} ;