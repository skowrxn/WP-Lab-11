Dear Student,

I regret to inform you that you've received only **5** out of 12 points for this assignment.
<details><summary>You have already managed to pass 5 tests, so that is encouraging!</summary>&emsp;☑&nbsp;[1p]&nbsp;Sudoku&nbsp;cnf&nbsp;post&nbsp;init<br>&emsp;☑&nbsp;[1p]&nbsp;Sudoku&nbsp;cnf&nbsp;at&nbsp;least&nbsp;one<br>&emsp;☑&nbsp;[1p]&nbsp;Sudoku&nbsp;cnf&nbsp;at&nbsp;most&nbsp;one<br>&emsp;☑&nbsp;[1p]&nbsp;Sudoku&nbsp;cnf&nbsp;exactly&nbsp;one<br>&emsp;☑&nbsp;[1p]&nbsp;Sudoku&nbsp;cnf&nbsp;possible&nbsp;propositions</details>

There still exist some issues that should be addressed before the deadline: **2025-06-09 15:00:00 CEST (+0200)**. For further details, please refer to the following list:

<details><summary>[1p] Group by works correctly &gt;&gt; not implemented yet</summary></details>
<details><summary>[1p] Sat solver finds correct solution &gt;&gt; not implemented yet</summary></details>
<details><summary>[1p] Sat solver respects timeout &gt;&gt; sat solver does not raise `TimeoutError` when necessary</summary></details>
<details><summary>[1p] Sudoku cnf every row contains unique values &gt;&gt; `_every_row_contains_unique_values` called `_at_most_one` 4 times, expected 10 times:</summary>&emsp;-&nbsp;puzzle:<br>-------------<br>|&nbsp;0,0&nbsp;|&nbsp;2,1&nbsp;|<br>|&nbsp;0,2&nbsp;|&nbsp;0,0&nbsp;|<br>-------------<br>|&nbsp;2,3&nbsp;|&nbsp;0,0&nbsp;|<br>|&nbsp;4,0&nbsp;|&nbsp;0,0&nbsp;|<br>-------------</details>
<details><summary>[1p] Sudoku cnf every col contains unique values &gt;&gt; &#x27;int&#x27; object is not iterable</summary></details>
<details><summary>[1p] Sudoku cnf every block contains unique values &gt;&gt; `_every_block_contains_unique_values` called `_at_most_one` 4 times, expected 10 times:</summary>&emsp;-&nbsp;puzzle:<br>-------------<br>|&nbsp;0,0&nbsp;|&nbsp;2,1&nbsp;|<br>|&nbsp;0,2&nbsp;|&nbsp;0,0&nbsp;|<br>-------------<br>|&nbsp;2,3&nbsp;|&nbsp;0,0&nbsp;|<br>|&nbsp;4,0&nbsp;|&nbsp;0,0&nbsp;|<br>-------------</details>
<details><summary>[1p] Sudoku cnf decode &gt;&gt; &#x27;int&#x27; object is not iterable</summary></details>

-----------
I remain your faithful servant\
_Bobot_\
_June 07, AD 2025, 15:20:00 (UTC)_