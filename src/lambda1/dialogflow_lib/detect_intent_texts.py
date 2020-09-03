import dialogflow_v2 as dialogflow

import logging
logger = logging.getLogger('bot')


def post_intent_texts(project_id, session_id, texts, language_code):
    """
    Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation.
    """

    result = []

    try:
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        logger.debug('Session path: {}\n'.format(session))

        for text in texts:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(session=session, query_input=query_input)

            logger.debug('=' * 20)
            logger.debug('Query text: {}'.format(response.query_result.query_text))
            logger.debug('Detected intent: {} (confidence: {})'.format(
                response.query_result.intent.display_name, response.query_result.intent_detection_confidence))
            logger.debug('Fulfillment text: {}'.format(response.query_result.fulfillment_text))

            data = {
                "query": response.query_result.query_text,
                "intent": response.query_result.intent.display_name,
                "confidence": response.query_result.intent_detection_confidence,
                "fulfillment": response.query_result.fulfillment_text
            }
            result.append(data)

    except Exception as e:
        logger.error('post_intent_texts(): {}'.format(e))

    return result
