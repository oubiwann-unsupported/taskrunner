from twisted.trial import unittest

from dreambuilder.command import CommandExpression as CExp


many_commands = CExp(
    CExp("pre-install check",
        CExp("install deps",
            CExp("install a dependency service",
                CExp("start service")
            ),
        ),
        halt_on_fail=True),
    CExp("do primary install",
        CExp("run a parallel process"),
        CExp("run another one"),
        CExp("run a thrid one"),
        CExp("run a fourth one, with a long chain",
            CExp("after 4th, do 4.1",
                CExp("after 4.1, do 4.2",
                    CExp("after 4.2, do 4.3",
                        CExp("after 4.3, do 4.4")
                    )
                )
            )
        ),
        CExp("run a fifth, with a big parallel batch afterwards",
            CExp("batch job 1"),
            CExp("batch job 2"),
            CExp("batch job 3"),
            CExp("batch job 4"),
            CExp("batch job 5"),
            CExp("batch job 6"),
            CExp("batch job 7"),
            CExp("batch job 8"),
            CExp("batch job 9"),
            CExp("batch job 10"),
            CExp("batch job 11"),
            CExp("batch job 12")
        )
    ),
    CExp("post-install check"),
)


class CommandExpressionTestCase(unittest.TestCase):
    """
    """
    def test_simple(self):
        simple_command = CExp("do it")
        self.assertEqual(simple_command.command, "do it")
