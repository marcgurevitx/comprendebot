import asyncio

import click

from botcommon.models import Phrase


@click.command()
@click.option("-a", "--accept-similar", "accept_similar", is_flag=True)
@click.argument("phrases_file", type=click.File())
def botaddphrases(phrases_file, accept_similar):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_add_phrases(phrases_file, accept_similar))


async def async_add_phrases(phrases_file, accept_similar):
    n_added = 0
    n_rejected = 0
    n_already = 0
    for line in phrases_file:
        line = line.strip()
        if line:
            click.echo(f"{line} -- ", nl=False)
            similar_phrases, normalized_text = await Phrase.find_similar(line)
            if similar_phrases:
                similar_phrases.sort(key=lambda p: p.similarity, reverse=True)

                if similar_phrases[0].similarity == 1.0:
                    n_already += 1
                    click.secho("already there", fg="yellow")
                    continue

                if not accept_similar:
                    click.echo()
                    click.secho("  Similar phrases found:", fg="yellow")
                    for phrase in similar_phrases:
                        click.secho(f"  * {phrase.phrase.row} ", nl=False)
                        click.secho(f"(similarity {phrase.similarity})", fg="yellow")
                    if not click.confirm("Add anyway?"):
                        n_rejected += 1
                        click.secho("rejected", fg="red")
                        continue

            await Phrase.add_from_cli(line, normalized_text)
            n_added += 1
            click.secho("added", fg="green")
    click.echo(f"Done, added [{n_added}], rejected [{n_rejected}], was already there [{n_already}]")
